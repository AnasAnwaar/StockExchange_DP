from src.services.db_manager import DatabaseManager
from src.models.employee import EmployeeBuilder

class EmployeeService:
    def __init__(self):
        self.db = DatabaseManager().get_connection()

    def add_employee(self, id_number, name, email, phone, address, department, designation, date_of_joining):
        employee_id = f"{department}--{id_number}"  # Generate EmployeeID

        cursor = self.db.cursor()
        try:
            builder = EmployeeBuilder()
            builder.set_employee_id(employee_id).set_name(name).set_email(email).set_phone(phone)
            builder.set_address(address).set_department(department).set_designation(designation)
            builder.set_date_of_joining(date_of_joining)
            employee = builder.build()

            cursor.execute("""
                INSERT INTO Employee (EmployeeID, Name, Email, Phone, Address, Department, Designation, DateOfJoining)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                employee['EmployeeID'], employee['Name'], employee['Email'], employee['Phone'],
                employee['Address'], employee['Department'], employee['Designation'], employee['DateOfJoining']
            ))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to add employee: {str(e)}")

    def list_employees(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT EmployeeID, Name, Email, Phone, Address, Department, Designation, DateOfJoining FROM Employee")
        return [{"EmployeeID": row[0], "Name": row[1], "Email": row[2], "Phone": row[3],
                 "Address": row[4], "Department": row[5], "Designation": row[6], "DateOfJoining": row[7]}
                for row in cursor.fetchall()]
