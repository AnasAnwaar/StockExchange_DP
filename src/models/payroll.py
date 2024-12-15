from decimal import Decimal
from src.services.db_manager import DBManager
from src.strategies.payroll_strategy import PayrollStrategy
from src.strategies.salary_pay import SalaryPayStrategy


class Payroll:
    """
    Represents a payroll record, integrating strategy design for pay calculations.
    """

    def __init__(self, employee_id, base_salary, bonus=0, deductions=0, strategy=None):
        self.employee_id = employee_id
        self.base_salary = Decimal(base_salary) if not isinstance(base_salary, Decimal) else base_salary
        self.bonus = Decimal(bonus) if not isinstance(bonus, Decimal) else bonus
        self.deductions = Decimal(deductions) if not isinstance(deductions, Decimal) else deductions
        self.strategy = strategy or SalaryPayStrategy()  # Default strategy if none is provided

    @property
    def net_pay(self):
        """
        Calculate net pay using the provided strategy.
        """
        if not self.strategy:
            raise ValueError("No payroll calculation strategy set.")
        return self.strategy.calculate_pay(self.base_salary, self.bonus, self.deductions)

    def set_strategy(self, strategy):
        """
        Dynamically change the payroll calculation strategy.
        """
        self.strategy = strategy

    @staticmethod
    def from_dict(record, strategy=None):
        """
        Create a Payroll object from a database record dictionary with a strategy.
        """
        return Payroll(
            employee_id=record.get('EmployeeID'),
            base_salary=Decimal(record.get('BaseSalary', 0)),
            bonus=Decimal(record.get('Bonus', 0)),
            deductions=Decimal(record.get('Deductions', 0)),
            strategy=strategy
        )

    @classmethod
    def fetch_all(cls, strategy=None):
        """
        Fetch all payroll records from the database, applying the given strategy.
        :return: List of Payroll objects.
        """
        try:
            db = DBManager()
            cursor = db.get_cursor()
            cursor.execute("SELECT EmployeeID, BaseSalary, Bonus, Deductions FROM Payroll")
            records = cursor.fetchall()
            if not records:
                print("No payroll records found.")
                return []
            columns = [column[0] for column in cursor.description]
            return [cls.from_dict(dict(zip(columns, row)), strategy) for row in records]
        except Exception as e:
            print(f"Error fetching payroll records: {e}")
            return []

    @classmethod
    def fetch_by_employee_id(cls, employee_id, strategy=None):
        """
        Fetch payroll record for a specific employee, applying the given strategy.
        :param employee_id: The ID of the employee.
        :return: Payroll object or None if no record is found.
        """
        try:
            db = DBManager()
            cursor = db.get_cursor()
            cursor.execute("SELECT EmployeeID, BaseSalary, Bonus, Deductions FROM Payroll WHERE EmployeeID = ?", (employee_id,))
            record = cursor.fetchone()
            if not record:
                print(f"No payroll record found for EmployeeID: {employee_id}")
                return None
            columns = [column[0] for column in cursor.description]
            return cls.from_dict(dict(zip(columns, record)), strategy)
        except Exception as e:
            print(f"Error fetching payroll for EmployeeID {employee_id}: {e}")
            return None

    @classmethod
    def add_payroll_record(cls, employee_id, base_salary, bonus=0, deductions=0):
        """
        Add a new payroll record to the database.
        :param employee_id: The ID of the employee.
        :param base_salary: The base salary of the employee.
        :param bonus: The bonus amount (default: 0).
        :param deductions: The deductions amount (default: 0).
        """
        if not employee_id or Decimal(base_salary) < 0 or Decimal(bonus) < 0 or Decimal(deductions) < 0:
            print(f"Invalid payroll data: EmployeeID={employee_id}, BaseSalary={base_salary}, Bonus={bonus}, Deductions={deductions}")
            return

        try:
            db = DBManager()
            cursor = db.get_cursor()
            cursor.execute(
                """
                INSERT INTO Payroll (EmployeeID, BaseSalary, Bonus, Deductions)
                VALUES (?, ?, ?, ?)
                """,
                (employee_id, float(base_salary), float(bonus), float(deductions))
            )
            db.get_connection().commit()
            print(f"Payroll record added for EmployeeID {employee_id}.")
        except Exception as e:
            print(f"Error adding payroll record for EmployeeID {employee_id}: {e}")

    @classmethod
    def update_payroll_record(cls, employee_id, base_salary=None, bonus=None, deductions=None):
        """
        Update an existing payroll record.
        :param employee_id: The ID of the employee.
        :param base_salary: The updated base salary (optional).
        :param bonus: The updated bonus amount (optional).
        :param deductions: The updated deductions amount (optional).
        """
        if not employee_id:
            print("EmployeeID is required to update payroll record.")
            return

        try:
            db = DBManager()
            cursor = db.get_cursor()

            update_fields = []
            update_values = []

            if base_salary is not None:
                update_fields.append("BaseSalary = ?")
                update_values.append(float(base_salary))

            if bonus is not None:
                update_fields.append("Bonus = ?")
                update_values.append(float(bonus))

            if deductions is not None:
                update_fields.append("Deductions = ?")
                update_values.append(float(deductions))

            if not update_fields:
                print("No fields to update for EmployeeID:", employee_id)
                return

            update_query = f"UPDATE Payroll SET {', '.join(update_fields)} WHERE EmployeeID = ?"
            update_values.append(employee_id)

            cursor.execute(update_query, update_values)
            db.get_connection().commit()
            print(f"Payroll record updated for EmployeeID {employee_id}.")
        except Exception as e:
            print(f"Error updating payroll record for EmployeeID {employee_id}: {e}")

    @classmethod
    def delete_all_records(cls):
        """
        Delete all records from the Payroll table.
        """
        try:
            db = DBManager()
            cursor = db.get_cursor()
            cursor.execute("DELETE FROM Payroll")
            db.get_connection().commit()
            print("All payroll records have been deleted.")
        except Exception as e:
            print(f"Error deleting all payroll records: {e}")

    @classmethod
    def delete_by_employee_id(cls, employee_id):
        """
        Delete payroll record for a specific employee.
        :param employee_id: The ID of the employee.
        """
        if not employee_id:
            print("EmployeeID is required to delete payroll record.")
            return

        try:
            db = DBManager()
            cursor = db.get_cursor()
            cursor.execute("DELETE FROM Payroll WHERE EmployeeID = ?", (employee_id,))
            db.get_connection().commit()
            print(f"Payroll record for EmployeeID {employee_id} has been deleted.")
        except Exception as e:
            print(f"Error deleting payroll record for EmployeeID {employee_id}: {e}")
