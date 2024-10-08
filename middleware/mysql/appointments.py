import os

from pathlib import Path

from singleton import Singleton

from .sql import Sql

import datetime

class Appointments(metaclass=Singleton):
    def __init__(self, db, cursor):
        self.m_db = db
        self.m_cursor = cursor
        parent_path = Path(__file__).parent
        self.m_sql = Sql(os.path.join(parent_path, "sql/appointments.sql"))

    def insert(self, id_doctor : int, id_patient : int, date : datetime):
        self.m_cursor.execute(
            self.m_sql.get_sql("INSERT"),
            (id_doctor, id_patient, date)
            )

        self.m_db.commit()

    def update(self, id : int, id_doctor : int, id_patient : int, date : datetime):
        self.m_cursor.execute(
            self.m_sql.get_sql("UPDATE"),
            (id_doctor, id_patient, date, id)
            )

        self.m_db.commit()

    def delete(self, id):
        self.m_cursor.execute(
            self.m_sql.get_sql("DELETE"), (id,)
            )

        self.m_db.commit()

    def select(self) -> tuple:
        self.m_cursor.execute(
            self.m_sql.get_sql("SELECT")
            )

        return self.m_cursor.fetchall()
