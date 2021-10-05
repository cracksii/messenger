from typing import Optional

from .client import Client


class Message:
    def __init__(self, data):
        # Define attributes for code intellisense
        self.content: str = ""
        self.author: Optional[Client] = None
        self.destination: str = ""
        self.__dict__.update(data)  # Set values

    def to_json(self):
        var = self.__dict__
        var["author"] = self.author.client_id
        return str(var)
