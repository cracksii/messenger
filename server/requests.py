import abc
import enum


class ServerRequestId(enum.IntEnum):
    FIRST_CONNECTION = 0


class ClientRequestId(enum.IntEnum):
    FIRST_CONNECTION = 0


class Request:
    def __init__(self, length: int, id: int, data: str, client, server):
        self.data = data
        self.id = id
        self.length = length

        self.client = client
        self.server = server


class BaseRequestHandler:
    @staticmethod
    @abc.abstractmethod
    def handle(request: Request):
        pass


