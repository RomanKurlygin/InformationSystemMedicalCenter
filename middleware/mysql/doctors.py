import os

from pathlib import Path

from singleton import Singleton

from .sql import Sql

class Doctors(metaclass=Singleton):
    def __init__(self, db, cursor):
        self.m_db = db
        self.m_cursor = cursor
        parent_path = Path(__file__).parent
        self.m_sql = Sql(os.path.join(parent_path, "sql/doctors.sql"))

    def insert(self, name : str, job : str, wage : int, phone : str):
        self.m_cursor.execute(
            self.m_sql.get_sql("INSERT"),
            (name, job, wage, phone)
            )

        self.m_db.commit()

    def update(self, id : int, name : str, job: str, wage : int, phone : str):
        self.m_cursor.execute(
            self.m_sql.get_sql("UPDATE"),
            (name, job, wage, phone, id)
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
