import mysql.connector

from .doctors import Doctors
from .patients import Patients
from .appointments import Appointments
from .medical_records import MedicalRecords

from .db_placeholder import DbPlaceholder

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="valeriyA2318",
  database='ismi'
)

cursor = mydb.cursor()

doctor = Doctors(mydb, cursor)

patient = Patients(mydb, cursor)

appointment = Appointments(mydb, cursor)

medical_record = MedicalRecords(mydb, cursor)
