# mysql_database_manager

import mysql.connector
from mysql.connector import Error
import pandas as pd

class MySQLDatabase:
    def __init__(self, host_name, user_name, user_password, db_name):
        self.connection = None
        self.host_name = host_name
        self.user_name = user_name
        self.user_password = user_password
        self.db_name = db_name

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host_name,
                user=self.user_name,
                passwd=self.user_password,
                database=self.db_name
            )
            print("MySQL Database connection successful")
        except Error as e:
            print(f"The error '{e}' occurred")

    def execute_query(self, query):
        if self.connection is not None and self.connection.is_connected():
            cursor = self.connection.cursor()
            try:
                cursor.execute(query)
                result = cursor.fetchall()
                columns = cursor.column_names
                cursor.close()
                return pd.DataFrame(result, columns=columns)
            except Error as e:
                print(f"The error '{e}' occurred")
                return pd.DataFrame()
        else:
            print("The connection to the database is not established")
            return pd.DataFrame()

    def close_connection(self):
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")
        else:
            print("The connection to the database is not established or already closed")

