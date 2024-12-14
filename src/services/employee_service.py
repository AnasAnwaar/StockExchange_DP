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
            self.cursor.execute(query, employee_id)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Error deleting employee: {str(e)}")

    def update_employee(self, employee_data):
        """
        Updates an employee's details in the database.
        :param employee_data: A dictionary containing updated employee details.
        """
        try:
            query = """
                UPDATE Employee
                SET Name = ?, Email = ?, Phone = ?, Address = ?, Department = ?, Designation = ?, DateOfJoining = ?
                WHERE EmployeeID = ?
            """
            self.cursor.execute(query, (
                employee_data["Name"], employee_data["Email"], employee_data["Phone"], employee_data["Address"],
                employee_data["Department"], employee_data["Designation"], employee_data["DateOfJoining"],
                employee_data["EmployeeID"]
            ))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Error updating employee: {str(e)}")

    def list_employees(self):
        """
        Fetches all employees from the database.
        :return: A list of dictionaries containing employee details.
        """
        try:
            query = "SELECT * FROM Employee"
            self.cursor.execute(query)
            columns = [column[0] for column in self.cursor.description]
            return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        except Exception as e:
            raise Exception(f"Error fetching employees: {str(e)}")
