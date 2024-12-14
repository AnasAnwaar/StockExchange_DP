import pyodbc
import threading


class DBManager:
    """
    Singleton class for managing the database connection.
    """
    _instance = None
    _lock = threading.Lock()  # To ensure thread-safe singleton implementation

    def __new__(cls, *args, **kwargs):
        with cls._lock:  # Ensure thread-safe initialization
            if not cls._instance:
                cls._instance = super(DBManager, cls).__new__(cls, *args, **kwargs)
                cls._instance._initialize(kwargs.get('connection_string'))
        return cls._instance

    def _initialize(self, connection_string=None):
        """
        Initialize the database connection (only once).
        :param connection_string: Optional custom connection string.
        """
        self.connection_string = connection_string or (
            "Driver={SQL Server};"
            "Server=DESKTOP-HS9F6CR\\MSSQLSERVER01;"
            "Database=EmployeeERP;"
            "Trusted_Connection=yes;"
        )
        try:
            self.connection = pyodbc.connect(self.connection_string)
            self.cursor = self.connection.cursor()
        except pyodbc.Error as e:
            raise Exception(f"Database connection failed: {e}")

    def get_connection(self):
        """
        Returns the database connection object.
        """
        return self.connection

    def get_cursor(self):
        """
        Returns the database cursor object.
        """
        return self.cursor

    def execute_query(self, query, params=None):
        """
        Executes a query with optional parameters.
        :param query: The SQL query to execute.
        :param params: Parameters to use in the query (default: None).
        :return: Query results, if any.
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return self.cursor
        except pyodbc.Error as e:
            self.connection.rollback()
            raise Exception(f"Query execution failed: {e}")

    def fetch_all(self, query, params=None):
        """
        Executes a query and fetches all results.
        :param query: The SQL query to execute.
        :param params: Parameters to use in the query (default: None).
        :return: List of results.
        """
        cursor = self.execute_query(query, params)
        return cursor.fetchall()

    def fetch_one(self, query, params=None):
        """
        Executes a query and fetches one result.
        :param query: The SQL query to execute.
        :param params: Parameters to use in the query (default: None).
        :return: Single result.
        """
        cursor = self.execute_query(query, params)
        return cursor.fetchone()

    def __enter__(self):
        """
        Context manager entry point.
        :return: The DBManager instance.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit point. Closes the connection.
        """
        self.close()

    def close(self):
        """
        Closes the database connection.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
