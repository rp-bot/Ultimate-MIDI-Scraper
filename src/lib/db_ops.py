"""This module helps CRUD operations"""
import __init__
import sqlite3


class GetData():
    def __init__(self, db, table_name):
        self.db = db
        self.table_name = table_name
        self.db_conn = sqlite3.connect(f'data/db/{self.db}.sqlite3')
        self.cursor = self.db_conn.cursor()

    def get_all(self):
        select_cmd = f"""SELECT * FROM {self.table_name}"""
        self.cursor.execute(select_cmd)
        return self.cursor.fetchall()

    def close_db(self):
        self.cursor.close()
        self.db_conn.close()
