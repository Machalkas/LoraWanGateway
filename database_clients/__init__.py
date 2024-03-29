from utils import logger
from abc import ABC, abstractmethod

def db_connect(func):
    def wrapper(self: DBClient, *args, **kargs):
        db_connect = self.connect(host=self.host, port=self.port, user=self.db_user, password=self.db_password, database=self.database)
        kargs["db_connection"] = db_connect
        return func(self, *args, **kargs)
    return wrapper


class DBClient(ABC):
    def __init__(self,
                 host: str,
                 port: str,
                 db_user: str,
                 db_password: str,
                 database: str = "default",
                 create_table_query: str = None,
                 table_columns: str = None,
                 table_name: str = None) -> None:
        if create_table_query is None and (table_columns is None or table_name is None):
            raise ValueError("create_table_query and (table_columns or table_name) can't both be None")
        elif create_table_query is not None:
            columns = create_table_query.split("(")[1]
            self.table_columns = [c.split()[0] for c in columns.split(",")]
            self.table_name = create_table_query.split("(")[0].split()[-1]
        else:
            self.table_columns = table_columns
            self.table_name = table_name
        self.host = host
        self.port = port
        self.db_user = db_user
        self.db_password = db_password
        self.database = database


    @abstractmethod
    def create_tables(self, db_connection, create_table_query):
        ...
    
    @abstractmethod
    def connect(self, host, port, user, password, database) -> None:
        ...

    @abstractmethod
    def save(self, data) -> None:
        ...

    # @abstractmethod
    # def get(self, data) -> None:
    #     ...