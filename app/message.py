from typing import Optional
import json
import time

from .client import Client


class Message:
    def __init__(self, data):
        # Define attributes for code intellisense
        self.content: str = ""
        self.author: Optional[Client] = None
        self.destination: str = ""
        self.timestamp: str = ""
        self.id: int = -1
        self.__dict__.update(data)  # Set values

    def to_json(self):
        vals = self.__dict__.copy()
        if isinstance(vals["author"], Client):
            vals.update({"author": self.author.client_id})
        return json.dumps(vals)

    def prepare(self):
        vals = json.loads(self.to_json())
        if vals["timestamp"] == "":
            vals.update({"timestamp": time.strftime("%d.%m.%Y %H:%M:%S")})
        return json.dumps(vals)
