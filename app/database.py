import typing

import mysql.connector
import time

try:
    from .client import Client, QueryType
    from .party import Party
except ImportError:
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
        query = Client.to_sql_query(QueryType.INSERT, Client(username=username, key=key, status=status, image=image))
        print(query)
        return self._db.callproc(query[0], query[1:])

    def delete_client(self, client_id):
        query = Client.to_sql_query(QueryType.DELETE, client_id=client_id)
        print(query)
        return self._db.callproc(query[0], query[1:])

    def reset(self):
        self._db.callproc("Reset", ())
        time.sleep(1)

    def get_client(self, **kwargs):
        if len(kwargs) != 0:
            key = [_ for _ in kwargs.keys()][0]
            value = str([_ for _ in kwargs.values()][0]).replace("\"", "\\\"")
            query = Client.to_sql_query(QueryType.SELECT, where=f'{key}="{value}"')
            result = self._db.query(query)
            if len(result) == 0:
                return None
            return Client.from_sql_query(result[0])
        raise KeyError("**kwargs needs one key value pair key for the where statement")

    def update_client(self, **kwargs):
        if len(kwargs) == 2:
            where_key = [_ for _ in kwargs.keys()][0]
            where_value = [_ for _ in kwargs.values()][0]
            update_key = [_ for _ in kwargs.keys()][1].replace("new_", "")
            update_value = [_ for _ in kwargs.values()][1].replace("'", "\"")
            return self._db.query(Client.to_sql_query(QueryType.UPDATE, where=f'{where_key}="{where_value}"', update=f"{update_key}='{update_value}'"))
        raise KeyError("**kwargs needs one key value pair key for the where and update statement")

    def get_party(self, id: str):
        result = self._db.query(f"select * from parties where party_id={id}")
        if len(result) == 0:
            return None
        return Party.from_sql_query(result[0])


if __name__ == '__main__':
    db = MySQLDatabase(database="db", host="localhost", user="admin", password="5r4gXDwSfnxc9Wez", log_file=r"../database/log.sql")
    db.utility.add_client("TestUser", "TestKey", "coding an app", "/img.png")
    db.print("clients")
