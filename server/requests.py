import abc


class Request:
    def __init__(self, length: int, id: int, data: str, client, server):
        self.data = data
        self.id = id
        self.length = length

        self.client = client
        self.server = server

    def __str__(self):
        return f"<Request {'{'}id: {self.id}, data: {self.data}, client: {self.client}{'}'})>"

    def __repr__(self):
        return str(self)


class BaseRequestHandler:
    @staticmethod
    @abc.abstractmethod
    def handle(request: Request):
        pass


