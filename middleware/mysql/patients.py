import os

from pathlib import Path

from singleton import Singleton

from .sql import Sql

class Patients(metaclass=Singleton):
    def __init__(self, db, cursor):
        self.m_db = db
        self.m_cursor = cursor
        parent_path = Path(__file__).parent
        self.m_sql = Sql(os.path.join(parent_path, "sql/patients.sql"))

    def insert(self, name : str, phone : str, gender : bool, weight : float, height : float):
        self.m_cursor.execute(
            self.m_sql.get_sql("INSERT"),
            (name, phone, gender, weight, height)
            )

        self.m_db.commit()

    def update(self, id : int, name : str, phone : str, gender : bool, weight : float, height : float):
        self.m_cursor.execute(
            self.m_sql.get_sql("UPDATE"),
            (name, phone, gender, weight, height, id)
            )

        self.m_db.commit()

    def delete(self, id : int):
        self.m_cursor.execute(
            self.m_sql.get_sql("DELETE"), (id,)
            )

        self.m_db.commit()

    def select(self) -> tuple:
        self.m_cursor.execute(
            self.m_sql.get_sql("SELECT")
            )

        return self.m_cursor.fetchall()
