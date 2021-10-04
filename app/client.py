import enum
import typing

from . import __app__ as app_name, TableType as Tables

from server import Client as NetworkClient


class QueryType(enum.Enum):
    INSERT = 0,
    SELECT = 1,
    DELETE = 2,
    UPDATE = 3


class Client:
    """
    Representation of a client in the application
    """

    def __init__(self,
                 client_id: int = 0,
                 username: str = "None",
                 key: str = "None",
                 party_table: str = "None",
                 creation_date: str = "None",
                 last_seen: str = "None",
                 status: str = f"I am new to {app_name}",
                 image: str = "None",
                 network_client: NetworkClient = None,
                 in_db: bool = False):
        self.in_database = in_db
        self.client_id = client_id
        self.username = username
        self.key = key
        self.parties = party_table  # name of the table containing the party ids
        self.creation_date = creation_date
        self.last_seen = last_seen
        self.status = status
        self.image = image  # Path to the image
        self.settings = {}
        self.network_client = network_client

    def __str__(self):
        return str(vars(self))

    def __repr__(self):
        return f"('{self.client_id}', '{self.network_client.address[0]}', '{'closed' if self.network_client.closed else 'open'}')"

    @staticmethod
    def sample_client():
        return Client(15, "SampleNickname", "abcdefghijklmnopqrstuvwxyz123", "12.05.2020", "13.08.2021,23:20:10", "Holy Hasel", "C:/files/image123.png")

    @staticmethod
    def to_sql_query(query_type: QueryType, class_=None, **kwargs):
        if query_type == QueryType.INSERT:
            if not class_:
                raise Exception("No client instance given")

            class_.in_database = True
            return "AddClient", f"{class_.username}", f"{class_.key}", f"{class_.status}", f"{class_.image}"

        elif query_type == QueryType.SELECT:
            if "where" in kwargs.keys():
                return f"select * from {Tables.CLIENT} where {kwargs['where']}"

            return f"select * from {Tables.CLIENT}"

        elif query_type == QueryType.DELETE:
            if "client_id" in kwargs.keys():
                return "DeleteClient", "t", f"{kwargs['client_id']}"
            else:
                raise Exception("You have to specify an id to remove an entry")

        elif query_type == QueryType.UPDATE:
            if "update" in kwargs.keys() and "where" in kwargs.keys():
                return f"update {Tables.CLIENT} set {kwargs['update']} where {kwargs['where']}"
            else:
                raise Exception("You have to specify a where condition and a update statement to update an entry")

        else:
            raise Exception(f"No query available for query_type {query_type}")

    @staticmethod
    def from_sql_query(query: typing.Tuple):
        return Client(query[0], query[1], query[2], query[3], query[4], query[5], query[6], query[7], in_db=True)

    @staticmethod
    def from_network_client(network_client: NetworkClient):
        from .application import App
        for client in App.clients:
            if client.network_client == network_client:
                return client
        return None

# creation_date:    dd.mm.yyyy
# last_seen:        dd.mm.yyyy hh:mm:ss
