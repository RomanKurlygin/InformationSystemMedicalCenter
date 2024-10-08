import os

from pathlib import Path

from singleton import Singleton

from .sql import Sql

class MedicalRecords(metaclass=Singleton):
    def __init__(self, db, cursor):
        self.m_db = db
        self.m_cursor = cursor
        parent_path = Path(__file__).parent
        self.m_sql = Sql(os.path.join(parent_path, "sql/medical_records.sql"))

    def insert(self, id_patient : int, diagnosis : str):
        self.m_cursor.execute(
            self.m_sql.get_sql("INSERT"),
            (id_patient, diagnosis)
            )

        self.m_db.commit()

    def update(self, id : int, id_patient : int, diagnosis : str):
        self.m_cursor.execute(
            self.m_sql.get_sql("UPDATE"),
            (id_patient, diagnosis, id)
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
