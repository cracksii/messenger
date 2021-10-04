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
        return f"NetworkClient from '{self.address[0]}', Status: '{'closed' if self.closed  else 'open'}'"


class Client(BaseClient):
    request_handler = {}

    def __init__(self, socket: s.socket, address: typing.Tuple[str, int], server: Server, manual_handle=False):
        super().__init__(socket, address, server, manual_handle)
        self._socket.settimeout(2)

    def send(self, data: str, request_id=None, header_length=64):
        # print(f"{data} {request_id} {header_length}")
        length = Server.expand(str(len(data)).encode(), header_length)
        self._socket.send(length)
        if request_id is not None:
            self._socket.send(Server.expand(str(request_id.value).encode(), header_length))
        self._socket.send(data.encode())

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
                                    # print(self.server.server_request_ids)
                                    # print(isinstance(self.server.server_request_ids, enum.IntEnum))
                                    try:
                                        self.request_handler[self.server.server_request_ids(id)].handle(request)
                                    except KeyError:
                                        log(f"No handler found for id: '{id}'", LogLevel.ERROR, self)
                                    break
                            break
                else:
                    log(f"Disconnected unexpected", LogLevel.WARNING, self)
                    return
            except s.timeout:
                pass
            except (OSError, ConnectionResetError):
                if not self.closed:
                    log(f"Disconnected unexpected", LogLevel.WARNING, self)
                    return    
                else:
                    break
            except ValueError:
                log(f"ValueError occurred on client {self.address[0]}", LogLevel.ERROR)
                break
            except Exception as ex:
                exception = str(traceback.format_exc())
                log(f"Exception occurred on client {self.address[0]}: \"{exception}\"", LogLevel.ERROR)
                break
        log(f"Disconnected", clr=colorama.Fore.RED, client=self)

    @classmethod
    def add_handler(cls, request_id: enum.IntEnum, handler):
        Client.request_handler[request_id] = handler
