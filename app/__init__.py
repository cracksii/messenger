import enum


__app__ = "my favourite message app"


class TableType(enum.Enum):
    CLIENT = "clients",
    PARTY = "parties"
    PARTY_SUFFIX = "_parties"
    MEMBER_SUFFIX = "_members"

    def __str__(self):
        return self.value[0]


from .client import Client, QueryType
from .message import Message
from .database import MySQLDatabase
from .application import App
from .handlers import *
from .senders import *
from .party import Party
