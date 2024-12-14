from src.services.db_manager import DBManager


class Employee:
    """
    Represents an Employee entity.
    """

    def __init__(self, employee_id, name, email, phone, address, department, designation, date_of_joining):
        self.employee_id = employee_id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.department = department
        self.designation = designation
        self.date_of_joining = date_of_joining

    @staticmethod
    def _map_columns_to_attributes(record):
        """
        Maps database column names to Employee attribute names.
        """
        column_mapping = {
            'EmployeeID': 'employee_id',
            'Name': 'name',
            'Email': 'email',
            'Phone': 'phone',
            'Address': 'address',
            'Department': 'department',
            'Designation': 'designation',
            'DateOfJoining': 'date_of_joining',
        }
        return {column_mapping[key]: value for key, value in record.items()}

    @classmethod
    def fetch_all(cls):
        """
        Fetch all employees from the database.
        :return: List of Employee objects.
        """
        try:
            db = DBManager()
            cursor = db.get_cursor()
            cursor.execute(
                "SELECT EmployeeID, Name, Email, Phone, Address, Department, Designation, DateOfJoining FROM Employee"
            )
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            return [cls(**cls._map_columns_to_attributes(dict(zip(columns, row)))) for row in rows]
        except Exception as e:
            print(f"Error fetching employees: {e}")
            return []

    @classmethod
    def fetch_by_id(cls, employee_id):
        """
        Fetch an employee by their ID.
        :param employee_id: The Employee ID to fetch.
        :return: Employee object or None.
        """
        try:
            db = DBManager()
            cursor = db.get_cursor()
            cursor.execute(
                "SELECT EmployeeID, Name, Email, Phone, Address, Department, Designation, DateOfJoining FROM Employee WHERE EmployeeID = ?",
                (employee_id,),
            )
            columns = [column[0] for column in cursor.description]
            row = cursor.fetchone()
            return cls(**cls._map_columns_to_attributes(dict(zip(columns, row)))) if row else None
        except Exception as e:
            print(f"Error fetching employee by ID {employee_id}: {e}")
            return None

    @classmethod
    def fetch_by_name(cls, name):
        """
        Fetch an employee by their name.
        :param name: The Employee name to fetch.
        :return: Employee object or None.
        """
        try:
            db = DBManager()
            cursor = db.get_cursor()
            cursor.execute(
                "SELECT EmployeeID, Name, Email, Phone, Address, Department, Designation, DateOfJoining FROM Employee WHERE Name = ?",
                (name,),
            )
            columns = [column[0] for column in cursor.description]
            row = cursor.fetchone()
            return cls(**cls._map_columns_to_attributes(dict(zip(columns, row)))) if row else None
        except Exception as e:
            print(f"Error fetching employee by name {name}: {e}")
            return None

    @classmethod
    def add_employee(cls, employee_data):
        """
        Add a new employee to the database.
        :param employee_data: Dictionary containing employee details.
        """
        try:
            db = DBManager()
            cursor = db.get_cursor()
            cursor.execute(
                """
                INSERT INTO Employee (EmployeeID, Name, Email, Phone, Address, Department, Designation, DateOfJoining)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    employee_data['employee_id'],
                    employee_data['name'],
                    employee_data['email'],
                    employee_data['phone'],
                    employee_data['address'],
                    employee_data['department'],
                    employee_data['designation'],
                    employee_data['date_of_joining'],
                ),
            )
            db.get_connection().commit()
            print(f"Employee {employee_data['name']} added successfully.")
        except Exception as e:
            print(f"Error adding employee {employee_data['name']}: {e}")


class EmployeeBuilder:
    """
    Builder pattern for constructing Employee objects dynamically.
    """

    def __init__(self):
        self._employee = {}

    def set_employee_id(self, employee_id):
        self._employee['employee_id'] = employee_id
        return self

    def set_name(self, name):
        self._employee['name'] = name
        return self

    def set_email(self, email):
        self._employee['email'] = email
        return self

    def set_phone(self, phone):
        self._employee['phone'] = phone
        return self

    def set_address(self, address):
        self._employee['address'] = address
        return self

    def set_department(self, department):
        self._employee['department'] = department
        return self

    def set_designation(self, designation):
        self._employee['designation'] = designation
        return self

    def set_date_of_joining(self, date_of_joining):
        self._employee['date_of_joining'] = date_of_joining
        return self

    def build(self):
        """
        Build and return the constructed Employee dictionary.
        """
        required_fields = ['employee_id', 'name', 'department']
        for field in required_fields:
            if field not in self._employee:
                raise ValueError(f"Missing required field: {field}")
        return self._employee


class Department:
    """
    Represents a department containing multiple employees.
    """

    def __init__(self, name):
        self.name = name
        self.employees = []

    def add_employee(self, employee):
        self.employees.append(employee)

    def remove_employee(self, employee):
        self.employees.remove(employee)

    def list_employees(self):
        return self.employees

    def fetch_employees_from_db(self):
        try:
            db = DBManager()
            cursor = db.get_cursor()
            cursor.execute(
                "SELECT EmployeeID, Name, Email, Phone, Address, Department, Designation, DateOfJoining FROM Employee WHERE Department = ?",
                (self.name,),
            )
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            self.employees = [Employee(**Employee._map_columns_to_attributes(dict(zip(columns, row)))) for row in rows]
        except Exception as e:
            print(f"Error fetching employees for department {self.name}: {e}")

    def __str__(self):
        return f"Department: {self.name}, Employees: {[emp.name for emp in self.employees]}"
