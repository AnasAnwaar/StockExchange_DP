import tkinter as tk
from tkinter import ttk, messagebox
from src.services.employee_service import EmployeeService
from src.models.observer import Subject


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
    Screen to display all employees in a table format with action buttons.
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

        # Updated columns to include new fields
        columns = (
            "EmployeeID", "Name", "Email", "Phone", "Address", "Department", "Designation", "DateOfJoining",
            "Type", "BaseSalary", "HourlyRate", "CommissionRate", "HoursWorked", "TotalSales"
        )
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

        # Define column headings and widths
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        # Scrollbars
        vertical_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        horizontal_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vertical_scrollbar.set, xscroll=horizontal_scrollbar.set)

        vertical_scrollbar.pack(side="right", fill="y")
        horizontal_scrollbar.pack(side="bottom", fill="x")

        self.tree.pack(fill="both", expand=True)

        # Fetch employee data and populate the table
        self.load_employees()

        # Attach event listener for row selection
        self.tree.bind("<<TreeviewSelect>>", self.on_employee_select)

        # Action Buttons
        self.action_frame = tk.Frame(self)
        self.action_frame.pack(pady=20)

        # Update and Delete buttons (initially disabled)
        self.update_button = tk.Button(self.action_frame, text="Update Employee", font=("Arial", 16),
                                       command=self.update_employee, state="disabled")
        self.update_button.pack(side="left", padx=20)

        self.delete_button = tk.Button(self.action_frame, text="Delete Employee", font=("Arial", 16),
                                       command=self.delete_employee, state="disabled")
        self.delete_button.pack(side="left", padx=20)

        # Back Button
        tk.Button(self.action_frame, text="Back", font=("Arial", 16),
                  command=self.app.go_back).pack(side="left", padx=20)

    def load_employees(self):
        """
        Loads employees from the database and populates the Treeview.
        """
        try:
            for row in self.tree.get_children():
                self.tree.delete(row)

            employees = EmployeeService().list_employees()
            for emp in employees:
                self.tree.insert("", "end", values=(
                    emp["EmployeeID"], emp["Name"], emp["Email"], emp["Phone"], emp["Address"],
                    emp["Department"], emp["Designation"], emp["DateOfJoining"], emp["Type"],
                    emp["BaseSalary"], emp["HourlyRate"], emp["CommissionRate"],
                    emp["HoursWorked"], emp["TotalSales"]
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch employees: {str(e)}")

    def on_employee_select(self, event):
        """
        Handles employee selection from the Treeview and enables action buttons.
        """
        selected_item = self.tree.selection()
        if selected_item:
            self.update_button.config(state="normal")
            self.delete_button.config(state="normal")
        else:
            self.update_button.config(state="disabled")
            self.delete_button.config(state="disabled")

    def update_employee(self):
        """
        Opens a pop-up window for updating the selected employee.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            return

        # Get the selected employee data
        values = self.tree.item(selected_item[0], "values")
        employee_data = {col: values[idx] for idx, col in enumerate(self.tree["columns"])}

        # Open the UpdateEmployeeWindow
        UpdateEmployeeWindow(self, employee_data, self.load_employees)

    def delete_employee(self):
        """
        Deletes the selected employee from the database.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            return

        # Get the selected employee ID
        employee_id = self.tree.item(selected_item[0], "values")[0]

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete Employee ID: {employee_id}?")
        if confirm:
            try:
                EmployeeService().delete_employee(employee_id)
                self.load_employees()
                messagebox.showinfo("Success", f"Employee ID: {employee_id} deleted successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete employee: {str(e)}")


class UpdateEmployeeWindow(tk.Toplevel):
    """
    Pop-up window for updating employee details.
    """
    def __init__(self, parent, employee_data, refresh_callback):
        super().__init__(parent)
        self.title("Update Employee")
        self.geometry("700x600")
        self.refresh_callback = refresh_callback
        self.employee_data = employee_data

        # Fields for employee data
        self.fields = {}
        row = 0
        for key, value in self.employee_data.items():
            tk.Label(self, text=key, font=("Arial", 12)).grid(row=row, column=0, padx=10, pady=5, sticky="e")
            entry = tk.Entry(self, width=30)
            entry.insert(0, value)
            entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")
            self.fields[key] = entry
            row += 1

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)

        tk.Button(button_frame, text="Save Changes", font=("Arial", 12), bg="green", fg="white",
                  command=self.save_changes).pack(side="left", padx=10)
        tk.Button(button_frame, text="Discard Changes", font=("Arial", 12), bg="orange",
                  command=self.discard_changes).pack(side="left", padx=10)
        tk.Button(button_frame, text="Back", font=("Arial", 12), command=self.destroy).pack(side="left", padx=10)

    def save_changes(self):
        """
        Save updated employee details.
        """
        updated_data = {key: field.get() for key, field in self.fields.items()}
        try:
            EmployeeService().update_employee(updated_data)
            messagebox.showinfo("Success", "Employee details updated successfully.")
            self.destroy()
            self.refresh_callback()  # Refresh the table after saving changes
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update employee: {str(e)}")

    def discard_changes(self):
        """
        Reset fields to their original values.
        """
        for key, value in self.employee_data.items():
            self.fields[key].delete(0, tk.END)
            self.fields[key].insert(0, value)
