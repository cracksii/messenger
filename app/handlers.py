import enum
import json
import colorama
import hashlib

from server.logger import log, LogLevel
from server import BaseRequestHandler, Request

from .senders import ClientHandlerId
from .message import Message
from .party import Party
from .client import Client


class ServerHandlerId(enum.IntEnum):  # Messages send from the client to server are identified with this id
    FIRST_CONNECTION = 0,
    LOGIN = 1,
    MESSAGE_SEND = 2


def parse_json(js):
    try:
        return json.loads(js)
    except ValueError as ex:
        log(f"Error while parsing json: '{ex}'", LogLevel.ERROR)
        return None


class FirstConnectionHandler(BaseRequestHandler):
    @staticmethod
    def handle(request: Request):
        log(f"Connected", LogLevel.DEBUG, request.client, colorama.Fore.GREEN)
        request.client.send("", ClientHandlerId.FIRST_CONNECTION)


class LogInHandler(BaseRequestHandler):
    @staticmethod
    def handle(request: Request):
        from .application import App
        data = parse_json(request.data)
        if data and "username" in data and "key" in data:
            db = App.db.utility
            name, key = data["username"], hashlib.sha256(data["key"].encode("utf-8")).hexdigest()
            log(f"Username: '{name}', Key: '{key}'", LogLevel.EXT_DEBUG, request.client)
            client = db.get_client(username=data["username"])
            client.network_client = request.client
            if not client:
                log(f"{request.client.address[0]}: No database entry found for username '{name}'", LogLevel.ERROR)
            else:
                if client.key == key:
                    App.clients.append(client)
                    log(f"Connected as client {client.client_id}", clr=colorama.Fore.GREEN, client=request.client)
                    request.client.send("1", ClientHandlerId.LOGIN)
                    return
                else:
                    log(f"Key '{key}'({len(key)}) doesn't match key '{client.key}'({len(client.key)})", LogLevel.WARNING, request.client)
        else:
            log(f"Send incorrect data: '{request.data}'", LogLevel.DEBUG, request.client)
        request.client.send("0", ClientHandlerId.LOGIN)


class MessageSendHandler(BaseRequestHandler):
    @staticmethod
    def handle(request: Request):
        data = parse_json(request.data)
        data["author"] = Client.from_network_client(request.client)
        msg = Message(data)
        party = Party.get(msg.destination)
        party.send(msg)
