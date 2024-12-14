import tkinter as tk
from tkinter import ttk, messagebox
from src.services.employee_service import EmployeeService


class EmployeeScreen(tk.Frame):
    """
    Employee Management screen.
    """
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app  # Reference to the main application

        # Title
        tk.Label(self, text="Employee Management", font=("Arial", 30)).pack(pady=50)

        # Add New Employee Button
        tk.Button(self, text="Add New Employee", font=("Arial", 20),
                  command=self.add_employee_screen).pack(pady=20)

        # Display All Employees Button
        tk.Button(self, text="Display All Employees", font=("Arial", 20),
                  command=lambda: self.app.show_screen(DisplayEmployeesScreen)).pack(pady=20)

        # Back Button
        tk.Button(self, text="Back", font=("Arial", 20),
                  command=self.app.go_back).pack(pady=20)

    def add_employee_screen(self):
        """
        Opens a screen to add an employee (placeholder for now).
        """
        messagebox.showinfo("Add Employee", "Add Employee Screen Coming Soon!")


class DisplayEmployeesScreen(tk.Frame):
    """
    Screen to display all employees in a table format with a scrollbar.
    """
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app  # Reference to the main application

        # Title
        tk.Label(self, text="All Employees", font=("Arial", 30)).pack(pady=20)

        # Treeview for displaying employees
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=20)

        columns = ("EmployeeID", "Name", "Email", "Phone", "Address", "Department", "Designation", "DateOfJoining")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

        # Define column headings and widths
        tree.heading("EmployeeID", text="Employee ID")
        tree.heading("Name", text="Name")
        tree.heading("Email", text="Email")
        tree.heading("Phone", text="Phone")
        tree.heading("Address", text="Address")
        tree.heading("Department", text="Department")
        tree.heading("Designation", text="Designation")
        tree.heading("DateOfJoining", text="Date of Joining")

        tree.column("EmployeeID", width=100, anchor="center")
        tree.column("Name", width=150, anchor="center")
        tree.column("Email", width=200, anchor="center")
        tree.column("Phone", width=100, anchor="center")
        tree.column("Address", width=200, anchor="center")
        tree.column("Department", width=100, anchor="center")
        tree.column("Designation", width=150, anchor="center")
        tree.column("DateOfJoining", width=120, anchor="center")

        # Add a vertical scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        tree.pack(fill="both", expand=True)

        # Fetch employee data and populate the table
        try:
            employees = EmployeeService().list_employees()
            for emp in employees:
                tree.insert("", "end", values=(
                    emp["EmployeeID"], emp["Name"], emp["Email"], emp["Phone"],
                    emp["Address"], emp["Department"], emp["Designation"], emp["DateOfJoining"]
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch employees: {str(e)}")

        # Back Button
        tk.Button(self, text="Back", font=("Arial", 20),
                  command=self.app.go_back).pack(pady=20)
