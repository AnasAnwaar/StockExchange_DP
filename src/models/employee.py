# Builder Pattern: Constructs Employee objects dynamically
class EmployeeBuilder:
    def __init__(self):
        self._employee = {}

    def set_employee_id(self, employee_id):
        self._employee['EmployeeID'] = employee_id
        return self

    def set_name(self, name):
        self._employee['Name'] = name
        return self

    def set_email(self, email):
        self._employee['Email'] = email
        return self

    def set_phone(self, phone):
        self._employee['Phone'] = phone
        return self

    def set_address(self, address):
        self._employee['Address'] = address
        return self

    def set_department(self, department):
        self._employee['Department'] = department
        return self

    def set_designation(self, designation):
        self._employee['Designation'] = designation
        return self

    def set_date_of_joining(self, date_of_joining):
        self._employee['DateOfJoining'] = date_of_joining
        return self

    def build(self):
        # Return the constructed Employee dictionary
        return self._employee


# Composite Pattern: Manage groups of employees in a department
class Department:
    def __init__(self, name):
        self.name = name
        self.employees = []

    def add_employee(self, employee):
        self.employees.append(employee)

    def remove_employee(self, employee):
        self.employees.remove(employee)
