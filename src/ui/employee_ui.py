import tkinter as tk
from tkinter import ttk, messagebox
from src.services.employee_service import EmployeeService
from src.models.observer import Subject, Observer


class EmployeeScreen(tk.Frame):
    """
    Employee Management screen with options to add or view employees.
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
        Placeholder for the Add Employee Screen.
        """
        messagebox.showinfo("Add Employee", "Add Employee Screen Coming Soon!")


class DisplayEmployeesScreen(tk.Frame, Subject):
    """
    Screen to display all employees in a table format with a detail editor.
    Implements the Subject (Observable) pattern.
    """
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        Subject.__init__(self)
        self.app = app  # Reference to the main application

        # Title
        tk.Label(self, text="All Employees", font=("Arial", 30)).pack(pady=20)

        # Treeview for displaying employees
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=20)

        columns = ("EmployeeID", "Name", "Email", "Phone", "Address", "Department", "Designation", "DateOfJoining")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

        # Define column headings and widths
        self.tree.heading("EmployeeID", text="Employee ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Address", text="Address")
        self.tree.heading("Department", text="Department")
        self.tree.heading("Designation", text="Designation")
        self.tree.heading("DateOfJoining", text="Date of Joining")

        self.tree.column("EmployeeID", width=100, anchor="center")
        self.tree.column("Name", width=150, anchor="center")
        self.tree.column("Email", width=200, anchor="center")
        self.tree.column("Phone", width=100, anchor="center")
        self.tree.column("Address", width=200, anchor="center")
        self.tree.column("Department", width=100, anchor="center")
        self.tree.column("Designation", width=150, anchor="center")
        self.tree.column("DateOfJoining", width=120, anchor="center")

        # Add a vertical scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree.pack(fill="both", expand=True)

        # Fetch employee data and populate the table
        self.load_employees()

        # Attach event listener for row selection
        self.tree.bind("<<TreeviewSelect>>", self.on_employee_select)

        # Back Button
        tk.Button(self, text="Back", font=("Arial", 20),
                  command=self.app.go_back).pack(pady=20)

        # Detail Editor Section
        self.detail_editor = EmployeeDetailEditor(self, app)
        self.detail_editor.pack(fill="both", side="bottom", padx=20, pady=20)

        # Attach the editor as an observer
        self.attach(self.detail_editor)

    def load_employees(self):
        """
        Loads employees from the database and populates the Treeview.
        """
        try:
            employees = EmployeeService().list_employees()
            for emp in employees:
                self.tree.insert("", "end", values=(
                    emp["EmployeeID"], emp["Name"], emp["Email"], emp["Phone"],
                    emp["Address"], emp["Department"], emp["Designation"], emp["DateOfJoining"]
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch employees: {str(e)}")

    def on_employee_select(self, event):
        """
        Handles employee selection from the Treeview and notifies observers.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            return

        # Get the selected employee data
        values = self.tree.item(selected_item[0], "values")
        employee_data = {
            "EmployeeID": values[0],
            "Name": values[1],
            "Email": values[2],
            "Phone": values[3],
            "Address": values[4],
            "Department": values[5],
            "Designation": values[6],
            "DateOfJoining": values[7],
        }

        # Notify observers (e.g., the detail editor)
        self.notify(employee_data)


class EmployeeDetailEditor(tk.Frame, Observer):
    """
    A detail editor section to view and edit employee details.
    Implements the Observer pattern.
    """
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent, bg="lightgrey")
        self.app = app  # Reference to the main application

        # Initialize selected_employee attribute
        self.selected_employee = None

        # Input fields
        self.fields = {
            "EmployeeID": tk.Entry(self, state="disabled"),
            "Name": tk.Entry(self),
            "Email": tk.Entry(self),
            "Phone": tk.Entry(self),
            "Address": tk.Entry(self),
            "Department": tk.Entry(self),
            "Designation": tk.Entry(self),
            "DateOfJoining": tk.Entry(self)
        }

        # Layout for fields
        row, col = 0, 0
        for label, entry in self.fields.items():
            tk.Label(self, text=label, bg="lightgrey", font=("Arial", 12)).grid(row=row, column=col, padx=10, pady=5, sticky="e")
            entry.grid(row=row, column=col + 1, padx=10, pady=5, sticky="w")
            col += 2
            if col > 6:  # Move to the next row after 4 fields
                col = 0
                row += 1

        # Action Buttons
        button_frame = tk.Frame(self, bg="lightgrey")
        button_frame.grid(row=row + 1, column=0, columnspan=8, pady=10)

        tk.Button(button_frame, text="Delete Employee", bg="red", fg="white", font=("Arial", 12),
                  command=self.delete_employee).pack(side="left", padx=10)
        tk.Button(button_frame, text="Save Changes", bg="green", fg="white", font=("Arial", 12),
                  command=self.save_changes).pack(side="left", padx=10)
        tk.Button(button_frame, text="Discard Changes", bg="orange", font=("Arial", 12),
                  command=self.reset_fields).pack(side="left", padx=10)

    def update_data(self, data):
        """
        Updates the input fields when notified of a new selection.
        """
        self.selected_employee = data
        for key, value in data.items():
            if key in self.fields:
                self.fields[key].config(state="normal")
                self.fields[key].delete(0, tk.END)
                self.fields[key].insert(0, value)
                if key == "EmployeeID":  # Make EmployeeID uneditable
                    self.fields[key].config(state="disabled")

    def delete_employee(self):
        """
        Deletes the selected employee using the EmployeeService backend.
        """
        if not self.selected_employee:
            messagebox.showwarning("No Selection", "Please select an employee to delete.")
            return

        try:
            employee_id = self.selected_employee["EmployeeID"]
            EmployeeService().delete_employee(employee_id)
            messagebox.showinfo("Success", "Employee deleted successfully!")
            self.app.go_back()  # Navigate back to refresh
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_changes(self):
        """
        Saves changes to the employee's details using the EmployeeService backend.
        """
        try:
            updated_data = {key: field.get() for key, field in self.fields.items()}
            EmployeeService().update_employee(updated_data)
            messagebox.showinfo("Success", "Employee updated successfully!")
            self.app.go_back()  # Navigate back to refresh
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def reset_fields(self):
        """
        Resets fields to the original data.
        """
        if self.selected_employee:
            self.update_data(self.selected_employee)
