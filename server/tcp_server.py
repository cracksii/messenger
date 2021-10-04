import socket as s
import time
import threading

from .logger import *
from .requests import ServerRequestId


class Server:
    def __init__(self, address, client, server_request_ids=ServerRequestId, log_lvl: DebugLevel = DebugLevel.NO_DEBUGGING):
        self.address = address
        self.ip = address[0]
        self.port = address[1]
        self.address_family = s.AddressFamily.AF_INET6 if ':' in address[0] else s.AddressFamily.AF_INET
        self.client = client
        self.closed = False
        self.clients = []
        self.server_request_ids = server_request_ids
        self._socket = s.socket(self.address_family)
        self.listen_thread = None
        self.bind()
        log.log_lvl = log_lvl

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()

    def bind(self):
        self._socket.bind(self.address)

    def start(self):
        log(f"Started listening on {self.ip if self.address_family == s.AddressFamily.AF_INET else '[' + self.ip + ']'}:{self.port}")
        log(f"Log Level {log.log_lvl.name}\n")
        self.listen_thread = threading.Thread(target=self.listen)
        self.listen_thread.start()
        while True:
            time.sleep(0.25)

    def listen(self):
        try:
            while not self.closed:
                self._socket.listen()
                socket, address = self._socket.accept()
                client = self.client(socket, address, self, True)
                self.clients.append(client)
                threading.Thread(target=client.listen).start()
        except OSError:
            return

    def shutdown(self):
        self.closed = True
        print("")
        log("Stopping server")
        log("Disconnecting all clients")

        if len(self.clients) == 0:
            log("-")
        for client in self.clients:
            client.close()

        time.sleep(0.5)
        log("Done")
        self._socket.close()

    @staticmethod
    def expand(data: bytes, new_size: int) -> bytes:
        if new_size < len(data):
            raise ValueError("The expanded size is smaller, than the actual size")
        return data + b" " * (new_size - len(data))

    def disconnect(self, client):
        if not type(client) is self.client:
            raise ValueError("You are trying to remove a wrong class")
        self.clients.remove(client)
