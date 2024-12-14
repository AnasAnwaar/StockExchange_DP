from src.services.db_manager import DBManager


class Payroll:
    def __init__(self, employee_id, base_salary, bonus=0, deductions=0):
        self.employee_id = employee_id
        self.base_salary = base_salary
        self.bonus = bonus
        self.deductions = deductions

    @property
    def net_pay(self):
        return self.base_salary + self.bonus - self.deductions

    @classmethod
    def fetch_all(cls):
        """
        Fetch all payroll records from the database.
        """
        db = DBManager()
        cursor = db.get_cursor()
        cursor.execute("SELECT * FROM Payroll")
        return cursor.fetchall()

    @classmethod
    def add_payroll_record(cls, employee_id, base_salary, bonus=0, deductions=0):
        """
        Add a new payroll record to the database.
        """
        db = DBManager()
        cursor = db.get_cursor()
        cursor.execute(
            """
            INSERT INTO Payroll (EmployeeID, BaseSalary, Bonus, Deductions)
            VALUES (?, ?, ?, ?)
            """,
            (employee_id, base_salary, bonus, deductions)
        )
        db.get_connection().commit()
