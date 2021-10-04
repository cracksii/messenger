import enum

from server.logger import log, LogLevel
from server.requests import BaseRequestHandler, Request


class ClientHandlerId(enum.IntEnum):  # Messages send from the server to client are identified with this id
    FIRST_CONNECTION = 0,
    LOGIN = 1,
    MESSAGE_SEND = 2

