from typing import Tuple, List

from server import Server, Client as NetworkClient, DebugLevel

from .database import MySQLDatabase
from .handlers import *
from .client import Client


class App:
    db = MySQLDatabase
    clients: List[Client] = []

    @staticmethod
    def run(host: Tuple[str, int]):
        App.db = MySQLDatabase(database="db", user="admin", password="5r4gXDwSfnxc9Wez")
        with Server(host, NetworkClient, ServerHandlerId, DebugLevel.EXTENDED_DEBUGGING) as tcp:
            NetworkClient.add_handler(ServerHandlerId.FIRST_CONNECTION, FirstConnectionHandler)
            NetworkClient.add_handler(ServerHandlerId.LOGIN, LogInHandler)
            NetworkClient.add_handler(ServerHandlerId.MESSAGE_SEND, MessageSendHandler)
            tcp.start()
