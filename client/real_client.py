import socket
import time
from threading import Thread
import json


def send(data, mid):
    print(data)
    if not data:
        return

    if type(data) is str:
        data = data.encode()
    header = expand(str(len(data)).encode(), 64)
    mid = expand(str(mid).encode(), 64)
    # print(f"{header} {header.__len__()}")
    # print(f"{mid} {mid.__len__()}")
    sock.send(header)
    sock.send(mid)
    sock.send(data)


def expand(data: bytes, new_size: int) -> bytes:
    return data + b" " * (new_size - len(data))


def recv():
    length = int(sock.recv(64))
    id = int(sock.recv(64))
    body = sock.recv(length)
    print(f"{length} {id} {body}")


def listen():
    while True:
        recv()


class Message:
    def __init__(self, data):
        # Define attributes for code intellisense
        self.content: str = ""
        self.author = None
        self.destination: str = ""
        self.__dict__.update(data)  # Set values

    def to_json(self):
        var = self.__dict__
        var["author"] = self.author
        return json.dumps(var)

    def from_json(self, json_msg):
        self.__dict__.update(json.loads(json_msg))


username = input("username: ")
if username == "":
    username = "Other User"

password = input("password: ")
if password == "":
    password = "TestKey"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 5000))
send(str({"username": username, "key": password}).replace("'", '"'), 1)
Thread(target=recv).start()

# send('[3, 5, 8]', 3)

while True:
    time.sleep(0.5)
    content = input("Enter message: ")
    group = input("Enter group_id: ")

    msg = Message({"content": content, "destination": group})

    send(msg.to_json(), 2)

