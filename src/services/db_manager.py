import pyodbc

class DatabaseManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.connection = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=DESKTOP-HS9F6CR\MSSQLSERVER01;'
                'DATABASE=EmployeeERP;'
                'Trusted_Connection=yes;'
            )
        return cls._instance

    def get_connection(self):
        return self.connection
