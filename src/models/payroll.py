from src.services.db_manager import DBManager


class Payroll:
    """
    Represents a payroll record.
    """

    def __init__(self, employee_id, base_salary, bonus=0, deductions=0):
        self.employee_id = employee_id
        self.base_salary = base_salary
        self.bonus = bonus
        self.deductions = deductions

    @property
    def net_pay(self):
        """
        Calculate net pay as base salary + bonus - deductions.
        """
        return self.base_salary + self.bonus - self.deductions

    @staticmethod
    def from_dict(record):
        """
        Create a Payroll object from a database record dictionary.
        """
        return Payroll(
            employee_id=record.get('EmployeeID'),
            base_salary=record.get('BaseSalary'),
            bonus=record.get('Bonus', 0),
            deductions=record.get('Deductions', 0)
        )

    @classmethod
    def fetch_all(cls):
        """
        Fetch all payroll records from the database.
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
            return [cls.from_dict(dict(zip(columns, row))) for row in records]
        except Exception as e:
            print(f"Error fetching payroll records: {e}")
            return []

    @classmethod
    def fetch_by_employee_id(cls, employee_id):
        """
        Fetch payroll record for a specific employee.
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
            return cls.from_dict(dict(zip(columns, record)))
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
        if not employee_id or base_salary < 0 or bonus < 0 or deductions < 0:
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
                (employee_id, base_salary, bonus, deductions)
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
                update_values.append(base_salary)

            if bonus is not None:
                update_fields.append("Bonus = ?")
                update_values.append(bonus)

            if deductions is not None:
                update_fields.append("Deductions = ?")
                update_values.append(deductions)

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
