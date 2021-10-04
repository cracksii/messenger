from app import App

"""
1. The server sends and receives 64 bytes from the client indicating the length of the message
2. The server sends and receives another 64 bytes from the client containing a handler id
3. The server or client reads data from the stream and handles it with the given handler id

Request:
    Length: 64 bytes
    Id:     64 bytes
    Data:   Length bytes
"""


def main():
    App.run(("127.0.0.1", 5000))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass


# 100 users no messages no parties = 1.6mb
