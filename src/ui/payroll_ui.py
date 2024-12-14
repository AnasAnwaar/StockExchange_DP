import tkinter as tk
from tkinter import ttk, messagebox
from src.services.payroll_service import PayrollService
from src.strategies.salary_pay import SalaryPayStrategy
from src.models.payroll import Payroll
from src.models.employee import Employee


class PayrollScreen(tk.Frame):
    """
    Payroll Screen for managing payrolls.
    """

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.service = PayrollService(strategy=SalaryPayStrategy())  # Default strategy

        # Title
        tk.Label(self, text="Payroll Module", font=("Arial", 30)).pack(pady=20)

        # Employee Dropdown
        tk.Label(self, text="Select Employee:").pack()
        self.employee_var = tk.StringVar()
        self.employee_dropdown = ttk.Combobox(self, textvariable=self.employee_var, state="readonly", width=50)
        self.employee_dropdown.pack(pady=10)

        # Populate Dropdown
        self.populate_employee_dropdown()

        # Payroll Form
        tk.Label(self, text="Base Salary:").pack()
        self.base_salary_entry = tk.Entry(self, width=30)
        self.base_salary_entry.pack()

        tk.Label(self, text="Bonus:").pack()
        self.bonus_entry = tk.Entry(self, width=30)
        self.bonus_entry.pack()

        tk.Label(self, text="Deductions:").pack()
        self.deductions_entry = tk.Entry(self, width=30)
        self.deductions_entry.pack()

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Calculate and Save Payroll", command=self.calculate_and_save_payroll).pack(side="left", padx=10)
        tk.Button(button_frame, text="Clear All Records", command=self.clear_all_records, fg="red").pack(side="left", padx=10)

        # Result Label
        self.result_label = tk.Label(self, text="", font=("Arial", 12))
        self.result_label.pack()

        # Payroll Table with Scrollbar
        self.create_payroll_table()

    def populate_employee_dropdown(self):
        """
        Populate the dropdown menu with employee names.
        """
        try:
            employees = Employee.fetch_all()
            if employees:
                employee_names = [f"{emp.name} ({emp.department})" for emp in employees]
                self.employee_dropdown['values'] = employee_names
            else:
                self.employee_dropdown['values'] = ["No employees available"]
        except Exception as e:
            print(f"Error populating employee dropdown: {e}")
            self.employee_dropdown['values'] = ["Error fetching employees"]

    def calculate_and_save_payroll(self):
        """
        Calculate payroll and save the record.
        """
        selected_employee = self.employee_var.get()
        if not selected_employee:
            self.result_label.config(text="Please select an employee", fg="red")
            return

        employee_name = selected_employee.split(" (")[0]
        employee = Employee.fetch_by_name(employee_name)

        if not employee:
            self.result_label.config(text="Selected employee not found!", fg="red")
            return

        try:
            base_salary = float(self.base_salary_entry.get())
            bonus = float(self.bonus_entry.get())
            deductions = float(self.deductions_entry.get())

            # Check if payroll already exists
            existing_payroll = Payroll.fetch_by_employee_id(employee.employee_id)
            if existing_payroll:
                self.result_label.config(text=f"Payroll already exists for {employee_name}.", fg="red")
                return

            # Calculate Net Pay
            net_pay = self.service.calculate_pay(base_salary, bonus, deductions)

            # Save Payroll Record
            Payroll.add_payroll_record(employee.employee_id, base_salary, bonus, deductions)

            # Update Result and Table
            self.result_label.config(text=f"Net Pay for {employee_name}: {net_pay:.2f}", fg="green")
            self.update_payroll_table()
        except ValueError:
            self.result_label.config(text="Please enter valid numerical values.", fg="red")
        except Exception as e:
            print(f"Error saving payroll record: {e}")
            self.result_label.config(text="An error occurred while saving payroll.", fg="red")

    def create_payroll_table(self):
        """
        Create a table to display all payroll records with a scrollbar.
        """
        table_frame = tk.Frame(self)
        table_frame.pack(pady=20, fill="both", expand=True)

        # Treeview (table)
        columns = ("Employee Name", "Department", "Base Salary", "Bonus", "Deductions", "Net Pay")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=150)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        # Pack Table and Scrollbar
        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.update_payroll_table()

    def update_payroll_table(self):
        """
        Update the payroll table with the latest records.
        """
        try:
            # Clear the table
            for row in self.table.get_children():
                self.table.delete(row)

            # Fetch payroll records and display them
            payroll_records = Payroll.fetch_all()
            if not payroll_records:
                self.result_label.config(text="No payroll records available.", fg="blue")
                return

            for record in payroll_records:
                employee = Employee.fetch_by_id(record.employee_id)
                if employee:
                    self.table.insert(
                        "",
                        "end",
                        values=(
                            employee.name,
                            employee.department,
                            record.base_salary,
                            record.bonus,
                            record.deductions,
                            record.net_pay,
                        ),
                    )
                else:
                    print(f"Employee with ID {record.employee_id} not found.")
        except Exception as e:
            print(f"Error updating payroll table: {e}")
            self.result_label.config(text="Error updating payroll table.", fg="red")

    def clear_all_records(self):
        """
        Clear all payroll records from the database and refresh the table.
        """
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete all payroll records?")
        if confirm:
            try:
                Payroll.delete_all_records()
                self.update_payroll_table()
                self.result_label.config(text="All payroll records have been deleted.", fg="green")
            except Exception as e:
                print(f"Error deleting payroll records: {e}")
                self.result_label.config(text="Error deleting payroll records.", fg="red")
