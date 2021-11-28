import enum
import socket as s
import abc
import traceback
import typing

import colorama

from .logger import log, LogLevel
from .tcp_server import Server
from .requests import Request


class BaseClient:
    """
    The base class for clients. The server creates a new instance and a separate thread for each client.
    You have to put all the logic in the handle method. It should have a while loop depending on server.closed
    that stops receiving when the socket is closed. Class variables are:
        - self.socket
        - self.address
        - self.server
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, socket: s.socket, address: typing.Tuple[str, int], server: Server, manual_handle=False):
        self._socket = socket
        self.address = address
        self.server = server
        self.closed = False

        if not manual_handle:
            self.listen()

    def send(self, data: str, header_length=64):
        length = Server.expand(str(len(data)).encode(), header_length)
        self._socket.send(length)
        self._socket.send(data.encode())

    def close(self):
        self.closed = True
        self._socket.close()

    @abc.abstractmethod
    def listen(self):
        return

    def __repr__(self):
        return f"<NetworkClient {'{'}ip: '{self.address[0]}', status: '{'closed' if self.closed  else 'open'}'{'}'}>"


class Client(BaseClient):
    request_handler = {}
    show_disconnection_message = True

    def __init__(self, socket: s.socket, address: typing.Tuple[str, int], server: Server, manual_handle=False):
        super().__init__(socket, address, server, manual_handle)
        self._socket.settimeout(2)

    def send(self, data, request_id=None):
        msg = "" if request_id is None else str(request_id.value) + "\\/\\"
        # log(f"{data} {request_id.value} '{msg + data}'", LogLevel.EXT_DEBUG)
        self._socket.send((msg + str(data) + "\\/\\/\\").encode())

    def listen(self):
        while not self.closed:
            try:
                length = self._socket.recv(64)
                if length:
                    length = int(length.decode())

                    while True:
                        id = self._socket.recv(64)
                        if id:
                            id = int(id.decode())

                            while True:
                                data = self._socket.recv(length)
                                if data:
                                    data = data.decode()
                                    request = Request(length, id, data, self, self.server)
                                    # print(self.server.server_request_ids, id)
                                    # print(self.request_handler)
                                    try:
                                        request_handler = self.request_handler[self.server.server_request_ids(id)]
                                    except KeyError:
                                        log(f"No handler found for id: '{id}'", LogLevel.ERROR, self)
                                        break
                                    try:
                                        request_handler.handle(request)
                                    except:
                                        exception = str(traceback.format_exc()).split("\n", 1)[1]
                                        log(f"Exception occured on client '{self.address[0]}' in request_handler '{self.server.server_request_ids(id).name}':\n{exception}", LogLevel.ERROR)

                                    break
                            break
                else:
                    log(f"Lost connection", LogLevel.WARNING, self)
                    self.closed = True
                    return
            except s.timeout:
                pass
            except (OSError, ConnectionResetError):
                if not self.closed:
                    log(f"Lost connection", LogLevel.WARNING, self)
                    self.closed = True
                    return    
                else:
                    break
            except:
                exception = str(traceback.format_exc())
                log(f"Exception occurred on client {self.address[0]}: {exception}", LogLevel.ERROR)
                self.closed = True
                break
        if self.show_disconnection_message:
            log(f"Disconnected", clr=colorama.Fore.RED, client=self)

    def close(self, show_message: bool = True):
        self.show_disconnection_message = show_message
        super().close()

    @classmethod
    def add_handler(cls, request_id: enum.IntEnum, handler):
        Client.request_handler[request_id] = handler
