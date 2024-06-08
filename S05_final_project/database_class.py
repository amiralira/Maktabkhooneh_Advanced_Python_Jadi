from sqlalchemy import create_engine, text
# from sqlalchemy_utils import create_database, database_exists
from urllib.parse import quote_plus
from mysql.connector import connect, Error


class DataBase:
    user_name = "root"
    password = "1234"
    host = "localhost"
    port = "3306"
    database_name = "Maktabkhooneh_advanced_python_final_project"

    def __init__(self):
        self.engin = None
        self.user_name = DataBase.user_name
        self.password = quote_plus(DataBase.password)
        self.host = DataBase.host
        self.port = DataBase.port
        self.db_name = DataBase.database_name
        self.connection_string = "mysql+mysqlconnector://" + self.user_name + ":" + self.password + "@" + self.host + ":" + self.port
        self.create_database()

    def get_engine(self):
        return create_engine(self.connection_string)

    def create_database(self):
        # print(self.connection_string)
        self.engin = create_engine(self.connection_string)

        with self.engin.connect() as con:
            con.execute(text(f"CREATE DATABASE IF NOT EXISTS {self.db_name}"))

        self.engin = create_engine(self.connection_string + "/" + self.db_name)





