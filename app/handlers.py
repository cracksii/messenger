import enum
import json
import colorama
import hashlib
from typing import List

from server.logger import log, LogLevel
from server import BaseRequestHandler, Request

from .senders import ClientHandlerId
from .message import Message
from .party import Party
from .client import Client


class ServerHandlerId(enum.IntEnum):  # Messages send from the client to server are identified with this id
    FIRST_CONNECTION = 0
    LOGIN = 1
    MESSAGE_SEND = 2
    LOAD_MESSAGES = 3,
    GET_PROPERTY = 4


def parse_json(js):
    try:
        return json.loads(js)
    except ValueError as ex:
        log(f"Error while parsing json: '{ex}'", LogLevel.ERROR)
        return None


class FirstConnectionHandler(BaseRequestHandler):
    @staticmethod
    def handle(request: Request):
        log(f"Connected", LogLevel.DEBUG, request.client)
        request.client.send("1", ClientHandlerId.FIRST_CONNECTION)


class LogInHandler(BaseRequestHandler):
    @staticmethod
    def handle(request: Request):
        from .application import App
        data = parse_json(request.data)
        if data and "username" in data and "key" in data:
            db = App.db.utility
            name, key = data["username"], hashlib.sha256(data["key"].encode()).hexdigest()
            log(f"Username: '{name}', Key: '{key}'", LogLevel.EXT_DEBUG, request.client)
            client = db.get_client(username=data["username"])
            if not client:
                log(f"No database entry found for username '{name}'", LogLevel.ERROR, client=request.client)
            elif client.is_connected():
                log(f"Is already connected", LogLevel.WARNING, client=request.client)
            else:
                client.network_client = request.client
                if client.key == key:
                    App.clients.append(client)
                    log(f"Connected as client {client.client_id}", clr=colorama.Fore.GREEN, client=request.client)
                    request.client.send("1", ClientHandlerId.LOGIN)
                    request.client.send(client.client_id, ClientHandlerId.CLIENT_ID)
                    return
                else:
                    log(f"Key '{key}'({len(key)}) doesn't match key '{client.key}'({len(client.key)})", LogLevel.WARNING, request.client)
        else:
            log(f"Send incorrect data: '{request.data}'", LogLevel.DEBUG, request.client)
        request.client.send("0", ClientHandlerId.LOGIN)
        request.client.close(False)


class MessageSendHandler(BaseRequestHandler):
    @staticmethod
    def handle(request: Request):
        data = parse_json(request.data)
        if not data:
            return
        client = Client.from_network_client(request.client)
        if client:
            msg = Message(data)
            msg.author = client
            party = Party.get(msg.destination)
            if party:
                log(party, LogLevel.EXT_DEBUG)
                party.send(msg)
                request.client.send("1", ClientHandlerId.MESSAGE_SEND)
            else:
                log(f"Party {msg.destination} wasn't found", LogLevel.ERROR, request.client)
        else:
            # log("Send message without login", LogLevel.WARNING, request.client)
            request.client.send("0", ClientHandlerId.MESSAGE_SEND)


class MessageLoadHandler(BaseRequestHandler):
    """
    Gets all messages the client didn't receive from the database and sends them back
    """
    @staticmethod
    def handle(request: Request):
        from . import App
        client = Client.from_network_client(request.client)
        if client:
            data: dict = json.loads(request.data)
            parties: List[Party] = App.db.utility.get_all_parties(client.client_id)
            # log(data, LogLevel.EXT_DEBUG)
            for party in parties:
                messages = party.get_messages_since(data[str(party.party_id)])
                for msg in messages:
                    request.client.send(msg.to_json(), ClientHandlerId.MESSAGE_SEND)
        else:
            log("Client wasn't found", LogLevel.ERROR)
            request.client.send("0", ClientHandlerId.LOAD_MESSAGES)


class PropertyGetHandler(BaseRequestHandler):

    @staticmethod
    def handle(request: Request):
        from . import App
        client = Client.from_network_client(request.client)
        if client:
            props: dict = parse_json(request.data)
            if "property" in props:
                prop = props["property"]
                if "data" in props:
                    props.update(props["data"])
                    props.pop("data")
                log(props, LogLevel.EXT_DEBUG, client=client.network_client)
                if prop == "parties":
                    parties = [_.info() for _ in App.db.utility.get_all_parties(client.client_id)]
                    request.client.send(json.dumps(parties), ClientHandlerId.GET_PROPERTY)
                elif prop == "messages" and "partyId" in props:
                    messages = [_.to_json() for _ in App.db.utility.get_party(props["partyId"]).get_messages_since(0)]
                    request.client.send(json.dumps(messages), ClientHandlerId.GET_PROPERTY)
                elif prop == "username" and "id" in props:
                    username = App.db.utility.get_client(client_id=props["id"]).username
                    request.client.send(username, ClientHandlerId.GET_PROPERTY)
                else:
                    request.client.send("0", ClientHandlerId.GET_PROPERTY)
        else:
            request.client.send("0", ClientHandlerId.GET_PROPERTY)


# Answering on a request with 1 if the communication is request -> response like. That way we can show if the request
# succeeded or not. If the response is not true or false we don't respond with a status code

# receiving a 1 usually means everything is fine, while receiving a 0 means the operation couldn't finished as planned
