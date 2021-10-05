import typing

import colorama
import mysql.connector
import time

from server import LogLevel, log

try:
    from . import TableType
    from .client import Client, QueryType
    from .party import Party
except ImportError:
    from app import TableType
    from app.client import Client, QueryType
    from app.party import Party


class MySQLDatabase:
    def __init__(self, database, password, host="localhost", user="root", log_file=r"database\log.sql"):
        self.name = database
        self.host = host
        self._db = mysql.connector.connect(
            host=host,
            user=user,
            database=database,
            password=password
        )
        self.log_file = log_file
        self.utility = DatabaseUtility(self)

    def __str__(self):
        rows = "\n" + "\n".join([str(_) for _ in self.query(f"select * from clients")])
        return f"Database '{self.name}' on '{self.host}' {rows if len(rows) > 1 else ''}"

    def query(self, sql):
        try:
            # print(sql)
            cursor = self._db.cursor(buffered=True)

            with open(self.log_file, "a") as f:
                f.write(f"{sql}{' ' * (99 - len(sql))}# {time.strftime('%Y.%m.%d %H:%M:%S')}\n")
                f.close()

            cursor.execute(sql, multi=False)
            self._db.commit()
            return [_ for _ in cursor]
        except Exception as e:
            raise Exception(f"{e}\n{sql}")

    def callproc(self, name, args: typing.Tuple):
        cursor = self._db.cursor(buffered=True)
        with open(self.log_file, "a") as f:
            sql = f"call {name}{args}"
            f.write(f"{sql}{' ' * (99 - len(sql))}# {time.strftime('%Y.%m.%d %H:%M:%S')}\n")
            f.close()
        cursor.callproc(name, args)
        return [_.fetchall()[0] for _ in cursor.stored_results()]

    def print(self, table: str):
        res = self.query(f"select * from {table}")
        for i in res:
            print(i)
        if len(res) == 0:
            print(f"Table '{table}' contains no values")


class DatabaseUtility:
    def __init__(self, database: MySQLDatabase):
        self._db = database

    def add_client(self, username, key, status, image):
        c = Client(username=username, key=key, status=status, image=image)
        query = Client.to_sql_query(QueryType.INSERT, c, self._db)
        res = []
        for q in query[:-1]:
            res.append(self._db.query(q))
        log(f"Added client {query[-1]} ('{username}', '{key}')", LogLevel.DEBUG)
        return c.client_id

    def delete_client(self, client_id):
        query = Client.to_sql_query(QueryType.DELETE, client_id=client_id)
        print(query)
        return self._db.callproc(query[0], query[1:])

    def reset(self):
        self._db.callproc("Reset", ())
        time.sleep(1)

    def get_client(self, **kwargs):
        # get_client(client_id=10)
        if len(kwargs) != 0:
            key = [_ for _ in kwargs.keys()][0]
            value = str([_ for _ in kwargs.values()][0]).replace("\"", "\\\"")
            query = Client.to_sql_query(QueryType.SELECT, where=f'{key}="{value}"')
            result = self._db.query(query)
            if len(result) == 0:
                log(f"Client with {key}={value} wasn't found", LogLevel.ERROR)
                return None
            return Client.from_sql_query(result[0])
        raise KeyError("**kwargs needs one key value pair key for the where statement")

    def update_client(self, **kwargs):
        # update_client(client_id=5, username="Wasd")
        if len(kwargs) == 2:
            where_key = [_ for _ in kwargs.keys()][0]
            where_value = [_ for _ in kwargs.values()][0]
            update_key = [_ for _ in kwargs.keys()][1].replace("new_", "")
            update_value = [_ for _ in kwargs.values()][1].replace("'", "\"")
            return self._db.query(Client.to_sql_query(QueryType.UPDATE, where=f'{where_key}="{where_value}"',
                                                      update=f"{update_key}='{update_value}'"))
        raise KeyError("**kwargs needs one key value pair key for the where and update statement")

    def add_party(self, name: str, description: str, owner: int, members: typing.List[int]):
        try:
            if self._db.query(f"select party_id from {TableType.PARTY.value} where name='{name}' and owner='{owner}'")[0][0]:
                log(f"Can't create party '{name}' owner '{owner}' already owns a party named like this", LogLevel.WARNING, clr=colorama.Fore.RED)
                return
        except IndexError:
            pass

        self._db.query(f"insert into {TableType.PARTY.value} (name, owner, description, creation_date) values('{name}', '{owner}', '{description}', '{time.strftime('%d.%m.%Y')}')")
        party_id = self._db.query(f"select party_id from {TableType.PARTY.value} where name='{name}' and owner='{owner}' and description='{description}'")[0][0]
        self._db.query(f"create table {party_id}{TableType.MEMBER_SUFFIX.value} (id int primary key auto_increment, client_id int)")

        if owner not in members:
            members.insert(0, owner)

        for member in members:
            self.add_to_party(party_id, self.get_client(client_id=member))

        log(f"Created party {party_id} name: '{name}' owner: '{owner}' members: {members}")

    def add_to_party(self, party_id: int, client: int):
        if client:
            self._db.query(f"insert into {client}{TableType.PARTY_SUFFIX.value} (party_id) values ({party_id})")
            self._db.query(f"insert into {party_id}{TableType.MEMBER_SUFFIX.value} (client_id) values ({client})")

    def get_party(self, party_id: int):
        result = self._db.query(f"select * from {TableType.PARTY.value} where party_id={party_id}")
        members = [_[0] for _ in self._db.query(f"select client_id from {party_id}{TableType.MEMBER_SUFFIX.value}")]
        if len(result) == 0:
            return None
        return Party.from_sql_query(result[0], members)


if __name__ == '__main__':
    db = MySQLDatabase(database="db", host="localhost", user="admin", password="5r4gXDwSfnxc9Wez", log_file=r"../database/log.sql")
    # db.utility.reset()
    db.utility.add_client("Other User", "TestKey", "online like a boss", "image.png")
    db.utility.add_to_party(1, 2)
    # db.utility.add_party("TestParty", "No desc", 1, [1])
    db.print("clients")
    db.print("parties")
