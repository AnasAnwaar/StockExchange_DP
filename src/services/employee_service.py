from src.services.db_manager import DBManager


class EmployeeService:
    """
    Service class for handling employee-related database operations.
    """

    def __init__(self):
        self.db_manager = DBManager()
        self.connection = self.db_manager.get_connection()
        self.cursor = self.db_manager.get_cursor()

    def delete_employee(self, employee_id):
        """
        Deletes an employee from the database based on their EmployeeID.
        :param employee_id: The ID of the employee to delete.
        """
        try:
            query = "DELETE FROM Employee WHERE EmployeeID = ?"
            self.cursor.execute(query, (employee_id,))
            self.connection.commit()
            print(f"Employee {employee_id} deleted successfully.")
        except Exception as e:
            self.connection.rollback()
            print(f"Error deleting employee {employee_id}: {str(e)}")
            raise Exception(f"Error deleting employee: {str(e)}")

    def update_employee(self, employee_data):
        """
        Updates an employee's details in the database.
        Supports dynamic updates based on provided fields.
        :param employee_data: A dictionary containing updated employee details.
        """
        try:
            # Ensure EmployeeID is present
            if "EmployeeID" not in employee_data or not employee_data["EmployeeID"]:
                raise ValueError("EmployeeID is required to update an employee.")

            # Validate and convert numeric fields
            numeric_fields = ["BaseSalary", "HourlyRate", "CommissionRate", "HoursWorked", "TotalSales"]
            for field in numeric_fields:
                if field in employee_data and employee_data[field] is not None:
                    try:
                        employee_data[field] = float(employee_data[field])
                    except ValueError:
                        raise ValueError(f"Invalid value for {field}: Must be a number.")

            # Build the update query dynamically based on provided fields
            update_fields = []
            update_values = []
            for key, value in employee_data.items():
                if key != "EmployeeID" and value is not None:  # Exclude EmployeeID and skip None values
                    update_fields.append(f"{key} = ?")
                    update_values.append(value)

            if not update_fields:
                raise ValueError("No valid fields provided to update.")

            update_values.append(employee_data["EmployeeID"])  # Add EmployeeID for the WHERE clause
            query = f"UPDATE Employee SET {', '.join(update_fields)} WHERE EmployeeID = ?"

            # Log the query and data for debugging
            print("Executing Query:", query)
            print("With Values:", update_values)

            self.cursor.execute(query, update_values)
            self.connection.commit()
            print(f"Employee {employee_data['EmployeeID']} updated successfully.")
        except ValueError as ve:
            print(f"Validation Error: {str(ve)}")
            raise ve
        except Exception as e:
            self.connection.rollback()
            print(f"Error executing update: {str(e)}")
            raise Exception(f"Error updating employee: {str(e)}")

    def update_employee_type_fields(self, employee_id, type_specific_fields):
        """
        Updates type-specific fields for employees (e.g., base salary, hourly rate, etc.).
        :param employee_id: The ID of the employee to update.
        :param type_specific_fields: A dictionary containing type-specific fields to update.
        """
        try:
            update_fields = []
            update_values = []
            for key, value in type_specific_fields.items():
                if value is not None:
                    update_fields.append(f"{key} = ?")
                    update_values.append(value)

            if not update_fields:
                raise ValueError("No type-specific fields provided to update.")

            update_values.append(employee_id)  # Add EmployeeID for the WHERE clause
            query = f"UPDATE Employee SET {', '.join(update_fields)} WHERE EmployeeID = ?"

            print("Executing Type-Specific Query:", query)
            print("With Values:", update_values)

            self.cursor.execute(query, update_values)
            self.connection.commit()
            print(f"Type-specific fields updated for EmployeeID: {employee_id}")
        except Exception as e:
            self.connection.rollback()
            print(f"Error updating type-specific fields for EmployeeID {employee_id}: {str(e)}")
            raise Exception(f"Error updating type-specific fields: {str(e)}")

    def add_employee(self, employee_data):
        """
        Adds a new employee to the database.
        :param employee_data: A dictionary containing employee details.
        """
        try:
            query = """
                INSERT INTO Employee (
                    EmployeeID, Name, Email, Phone, Address, Department, Designation, DateOfJoining, Type,
                    BaseSalary, HourlyRate, CommissionRate, HoursWorked, TotalSales
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, (
                employee_data["EmployeeID"], employee_data["Name"], employee_data["Email"], employee_data["Phone"],
                employee_data["Address"], employee_data["Department"], employee_data["Designation"],
                employee_data["DateOfJoining"], employee_data["Type"], employee_data.get("BaseSalary"),
                employee_data.get("HourlyRate"), employee_data.get("CommissionRate"),
                employee_data.get("HoursWorked"), employee_data.get("TotalSales")
            ))
            self.connection.commit()
            print(f"Employee {employee_data['EmployeeID']} added successfully.")
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding employee: {str(e)}")
            raise Exception(f"Error adding employee: {str(e)}")

    def list_employees(self):
        """
        Fetches all employees from the database.
        :return: A list of dictionaries containing employee details.
        """
        try:
            query = """
                SELECT EmployeeID, Name, Email, Phone, Address, Department, Designation, DateOfJoining, Type,
                       BaseSalary, HourlyRate, CommissionRate, HoursWorked, TotalSales
                FROM Employee
            """
            self.cursor.execute(query)
            columns = [column[0] for column in self.cursor.description]
            return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Error fetching employees: {str(e)}")
            raise Exception(f"Error fetching employees: {str(e)}")

    def fetch_employee_by_id(self, employee_id):
        """
        Fetches an employee by their EmployeeID.
        :param employee_id: The ID of the employee to fetch.
        :return: A dictionary containing the employee details, or None if not found.
        """
        try:
            query = """
                SELECT EmployeeID, Name, Email, Phone, Address, Department, Designation, DateOfJoining, Type,
                       BaseSalary, HourlyRate, CommissionRate, HoursWorked, TotalSales
                FROM Employee WHERE EmployeeID = ?
            """
            self.cursor.execute(query, (employee_id,))
            record = self.cursor.fetchone()
            if not record:
                print(f"No employee found with ID: {employee_id}")
                return None
            columns = [column[0] for column in self.cursor.description]
            return dict(zip(columns, record))
        except Exception as e:
            print(f"Error fetching employee by ID: {str(e)}")
            raise Exception(f"Error fetching employee by ID: {str(e)}")
