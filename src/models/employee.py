from src.services.db_manager import DBManager
from src.strategies.salary_pay import SalaryPayStrategy
from src.strategies.hourly_pay import HourlyPayStrategy
from src.strategies.commission_pay import CommissionPayStrategy

class Employee:
    """
    Represents an employee and includes functionality for determining payroll strategy.
    """

    def __init__(self, employee_id, name, department, type="salaried", 
                 hourly_rate=None, hours_worked=None, commission_rate=None, total_sales=None, base_salary=0.0):
        self.employee_id = employee_id
        self.name = name
        self.department = department
        self.type = type
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked
        self.commission_rate = commission_rate
        self.total_sales = total_sales
        self.base_salary = base_salary  # For salaried employees

    @staticmethod
    def from_dict(record):
        """
        Create an Employee object from a database record dictionary.
        """
        return Employee(
            employee_id=record.get('EmployeeID'),
            name=record.get('Name'),
            department=record.get('Department'),
            type=record.get('Type', 'salaried'),
            hourly_rate=record.get('HourlyRate'),
            hours_worked=record.get('HoursWorked'),
            commission_rate=record.get('CommissionRate'),
            total_sales=record.get('TotalSales'),
            base_salary=record.get('BaseSalary', 0.0)  # Default to 0.0 if not provided
        )

    @classmethod
    def fetch_all(cls):
        """
        Fetch all employees from the database.
        :return: List of Employee objects.
        """
        try:
            db = DBManager()
            cursor = db.get_cursor()
            cursor.execute("""
                SELECT EmployeeID, Name, Department, Type, HourlyRate, HoursWorked, CommissionRate, TotalSales, BaseSalary
                FROM Employee
            """)
            records = cursor.fetchall()
            if not records:
                print("No employees found.")
                return []
            columns = [column[0] for column in cursor.description]
            return [cls.from_dict(dict(zip(columns, row))) for row in records]
        except Exception as e:
            print(f"Error fetching employees: {e}")
            return []

    @classmethod
    def fetch_by_id(cls, employee_id):
        """
        Fetch an employee by their ID.
        :param employee_id: The ID of the employee.
        :return: Employee object or None if no record is found.
        """
        try:
            db = DBManager()
            cursor = db.get_cursor()
            cursor.execute("""
                SELECT EmployeeID, Name, Department, Type, HourlyRate, HoursWorked, CommissionRate, TotalSales, BaseSalary
                FROM Employee WHERE EmployeeID = ?
            """, (employee_id,))
            record = cursor.fetchone()
            if not record:
                print(f"No employee found with ID: {employee_id}")
                return None
            columns = [column[0] for column in cursor.description]
            return cls.from_dict(dict(zip(columns, record)))
        except Exception as e:
            print(f"Error fetching employee by ID {employee_id}: {e}")
            return None

    @classmethod
    def fetch_by_name(cls, name):
        """
        Fetch an employee by their name.
        :param name: The name of the employee.
        :return: Employee object or None if no record is found.
        """
        try:
            db = DBManager()
            cursor = db.get_cursor()
            cursor.execute("""
                SELECT EmployeeID, Name, Department, Type, HourlyRate, HoursWorked, CommissionRate, TotalSales, BaseSalary
                FROM Employee WHERE Name = ?
            """, (name,))
            record = cursor.fetchone()
            if not record:
                print(f"No employee found with name: {name}")
                return None
            columns = [column[0] for column in cursor.description]
            return cls.from_dict(dict(zip(columns, record)))
        except Exception as e:
            print(f"Error fetching employee by name {name}: {e}")
            return None

    @classmethod
    def update_salary(cls, employee_id, base_salary):
        """
        Updates the BaseSalary of a salaried employee in the database.
        """
        try:
            db = DBManager()
            cursor = db.get_cursor()
            cursor.execute("""
                UPDATE Employee
                SET BaseSalary = ?
                WHERE EmployeeID = ?
            """, (base_salary, employee_id))
            db.get_connection().commit()
            print(f"BaseSalary updated for EmployeeID: {employee_id}")
        except Exception as e:
            print(f"Error updating salary for EmployeeID {employee_id}: {e}")
            raise RuntimeError(f"Failed to update salary for EmployeeID {employee_id}")

    @classmethod
    def update_hourly_rate(cls, employee_id, hourly_rate):
        """
        Updates the HourlyRate of an hourly employee in the database.
        """
        try:
            db = DBManager()
            cursor = db.get_cursor()
            cursor.execute("""
                UPDATE Employee
                SET HourlyRate = ?
                WHERE EmployeeID = ?
            """, (hourly_rate, employee_id))
            db.get_connection().commit()
            print(f"HourlyRate updated for EmployeeID: {employee_id}")
        except Exception as e:
            print(f"Error updating hourly rate for EmployeeID {employee_id}: {e}")
            raise RuntimeError(f"Failed to update hourly rate for EmployeeID {employee_id}")

    def determine_strategy(self):
        """
        Determine the payroll strategy based on the employee type.
        :return: An appropriate payroll strategy object.
        """
        if self.type == "hourly":
            if self.hourly_rate is None or self.hours_worked is None:
                raise ValueError(f"Hourly employee {self.name} is missing required fields: HourlyRate or HoursWorked.")
            return HourlyPayStrategy(hourly_rate=self.hourly_rate, hours_worked=self.hours_worked)
        elif self.type == "commission":
            if self.commission_rate is None or self.total_sales is None:
                raise ValueError(f"Commission employee {self.name} is missing required fields: CommissionRate or TotalSales.")
            return CommissionPayStrategy(commission_rate=self.commission_rate, total_sales=self.total_sales)
        else:  # Default to salaried
            if self.base_salary is None:
                raise ValueError(f"Salaried employee {self.name} is missing the BaseSalary field.")
            return SalaryPayStrategy()
