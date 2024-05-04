
import sqlite3

from os import path

class DatabaseHandler:

    def __init__(self, dbFolder):
        self.dbPath = path.join(dbFolder, 'sql.db')

    def cursor(self, func):
        def wrapper(*args, **kwargs):
            cursor = self.connection.cursor()
            result = func(cursor, *args, **kwargs)
            cursor.close()

            return result
        return wrapper

    def connect(self):
        self.connection = sqlite3.connect(self.dbPath)

    def disconnect(self):
        if self.connection: self.connection.close()

    def generateTable(self):
        query = ''' CREATE TABLE BARCODES(
            BARCODE TEXT PRIMARY KEY NOT NULL,
            INFO TEXT NOT NULL
        )'''

        self.connection.execute('DROP TABLE IF EXISTS BARCODES')
        self.connection.execute(query)

    def fetch(self):
        items = self.connection.execute('SELECT * from BARCODES')
        return items

    def insert(self, itemJSON):
        barcode = itemJSON['barcode']
        query = f'INSERT INTO BARCODES VALUES ("{barcode}", "{itemJSON}")'
        self.connection.execute(query)
        self.connection.commit()