import sys
from MDBConnector import Database

from PySide6.QtCore import (Qt, QEvent, QObject, Signal, Slot)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget)

user="root",
password = '1234',
host='localhost',
port=3306,
database='py_script_test'

db = Database(user, password, host, port, database)

columns = [
    ['id', 'INT PRIMARY KEY NOT NULL AUTO_INCREMENT'],
    ['nome', 'CHAR(50)']
]

db.get_tables()
db.new_table('r', 'table1', columns=columns)
db.select_table('table1')

new_column = [
    ['testando', 'CHAR(50)']
]

db.add_column(new_column)
































