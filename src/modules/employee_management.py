import pyodbc

class EmployeeManagement:
    def __init__(self, connection):
        self.connection = connection

    # Fetch all employees from the database
    def fetch_all_employees(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Employee")
        employees = cursor.fetchall()
        cursor.close()
        return employees

    # Add a new employee to the database
    def add_employee(self, name, email, phone, address, department, designation, doj):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, email, phone, address, department, designation, doj))
        self.connection.commit()
        cursor.close()

    # Update an existing employee's details
    def update_employee(self, employee_id, name, email, phone, address, department, designation, doj):
        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE Employee
            SET Name = ?, Email = ?, Phone = ?, Address = ?, Department = ?, Designation = ?, DateOfJoining = ?
            WHERE EmployeeID = ?
        """, (name, email, phone, address, department, designation, doj, employee_id))
        self.connection.commit()
        cursor.close()

    # Delete an employee from the database
    def delete_employee(self, employee_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM Employee WHERE EmployeeID = ?", (employee_id,))
        self.connection.commit()
        cursor.close()
