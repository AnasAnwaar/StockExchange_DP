import pyodbc


class DBManager:
    """
    Singleton class for managing the database connection.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DBManager, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """
        Initialize the database connection (only once).
        """
        self.connection_string = (
            "Driver={SQL Server};"
            "Server=DESKTOP-HS9F6CR\\MSSQLSERVER01;"
            "Database=EmployeeERP;"
            "Trusted_Connection=yes;"
        )
        self.connection = pyodbc.connect(self.connection_string)
        self.cursor = self.connection.cursor()

    def get_connection(self):
        return self.connection

    def get_cursor(self):
        return self.cursor
