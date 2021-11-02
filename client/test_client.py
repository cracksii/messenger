import socket
import time


def send(data, mid):
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


NO_CONTENT = " "

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 5000))

time.sleep(1)

send(NO_CONTENT, 0)

length = int(sock.recv(64))
id = int(sock.recv(64))
body = sock.recv(length)
print(f"{length} {id} {body}")

send('{"username":"TestUser", "key":"TestKey"}', 1)

while True:
    length = int(sock.recv(64))
    id = int(sock.recv(64))
    body = sock.recv(length)
    print(f"{length} {id} {body}")
