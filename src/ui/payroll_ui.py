import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal
from src.models.employee import Employee
from src.models.payroll import Payroll
from src.services.payroll_service import PayrollService


class PayrollScreen(tk.Frame):
    """
    Payroll Screen for managing payrolls.
    """

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # Title
        tk.Label(self, text="Payroll Module", font=("Arial", 30)).pack(pady=20)

        # Employee Dropdown
        tk.Label(self, text="Select Employee:").pack()
        self.employee_var = tk.StringVar()
        self.employee_dropdown = ttk.Combobox(self, textvariable=self.employee_var, state="readonly", width=50)
        self.employee_dropdown.pack(pady=10)
        self.employee_dropdown.bind("<<ComboboxSelected>>", self.on_employee_selected)

        # Payroll Form
        self.create_payroll_form()

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Calculate and Save Payroll", command=self.calculate_and_save_payroll).pack(side="left", padx=10)
        tk.Button(button_frame, text="Clear All Records", command=self.clear_all_records, fg="red").pack(side="left", padx=10)
        tk.Button(button_frame, text="Back", command=self.go_back, fg="blue").pack(side="left", padx=10)

        # Result Label
        self.result_label = tk.Label(self, text="", font=("Arial", 12))
        self.result_label.pack()

        # Payroll Table with Scrollbar
        self.create_payroll_table()

        # Populate Employee Dropdown
        self.populate_employee_dropdown()

    def create_payroll_form(self):
        """
        Create the payroll form fields.
        """
        self.form_frame = tk.Frame(self)
        self.form_frame.pack(pady=10)

        # Dynamic Fields
        self.basic_salary_label = tk.Label(self.form_frame, text="Basic Salary:")
        self.basic_salary_entry = tk.Entry(self.form_frame, width=30)

        self.hourly_rate_label = tk.Label(self.form_frame, text="Hourly Rate:")
        self.hourly_rate_entry = tk.Entry(self.form_frame, width=30)

        self.working_hours_label = tk.Label(self.form_frame, text="Working Hours:")
        self.working_hours_entry = tk.Entry(self.form_frame, width=30)

        self.commission_rate_label = tk.Label(self.form_frame, text="Commission Rate:")
        self.commission_rate_value = tk.Label(self.form_frame, text="", fg="blue")
        self.sales_label = tk.Label(self.form_frame, text="Total Sales:")
        self.sales_entry = tk.Entry(self.form_frame, width=30)

        # General Fields
        tk.Label(self.form_frame, text="Bonus:").pack()
        self.bonus_entry = tk.Entry(self.form_frame, width=30)
        self.bonus_entry.pack()

        tk.Label(self.form_frame, text="Deductions:").pack()
        self.deductions_entry = tk.Entry(self.form_frame, width=30)
        self.deductions_entry.pack()

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

    def on_employee_selected(self, event):
        """
        Dynamically update form fields based on the selected employee type.
        """
        selected_employee = self.employee_var.get()
        if not selected_employee:
            return

        employee_name = selected_employee.split(" (")[0]
        employee = Employee.fetch_by_name(employee_name)

        if not employee:
            self.result_label.config(text="Selected employee not found!", fg="red")
            return

        # Clear dynamic fields
        self.clear_dynamic_fields()

        if employee.type == "salaried":
            # Display basic salary field for salaried employees
            self.basic_salary_label.pack()
            self.basic_salary_entry.delete(0, tk.END)
            self.basic_salary_entry.insert(0, f"{Decimal(employee.base_salary):.2f}")
            self.basic_salary_entry.pack()

        elif employee.type == "hourly":
            # Display hourly rate and working hours for hourly employees
            self.hourly_rate_label.pack()
            self.hourly_rate_entry.delete(0, tk.END)
            self.hourly_rate_entry.insert(0, f"{Decimal(employee.hourly_rate):.2f}")
            self.hourly_rate_entry.pack()

            self.working_hours_label.pack()
            self.working_hours_entry.pack()

        elif employee.type == "commission":
            # Display commission rate and sales for commission-based employees
            self.commission_rate_label.pack()
            self.commission_rate_value.config(text=f"{Decimal(employee.commission_rate):.2%}")
            self.commission_rate_value.pack()

            self.sales_label.pack()
            self.sales_entry.pack()

    def clear_dynamic_fields(self):
        """
        Clear all dynamic fields in the payroll form.
        """
        self.basic_salary_label.pack_forget()
        self.basic_salary_entry.pack_forget()
        self.hourly_rate_label.pack_forget()
        self.hourly_rate_entry.pack_forget()
        self.working_hours_label.pack_forget()
        self.working_hours_entry.pack_forget()
        self.commission_rate_label.pack_forget()
        self.commission_rate_value.pack_forget()
        self.sales_label.pack_forget()
        self.sales_entry.pack_forget()

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
            # Get bonus and deductions
            bonus = Decimal(self.bonus_entry.get())
            deductions = Decimal(self.deductions_entry.get())
            base_salary = Decimal(0)
            working_hours = Decimal(0)
            total_sales = Decimal(0)

            # Update employee data based on their type
            if employee.type == "salaried":
                base_salary = Decimal(self.basic_salary_entry.get())
                employee.base_salary = base_salary
                Employee.update_salary(employee.employee_id, base_salary)

            elif employee.type == "hourly":
                hourly_rate = Decimal(self.hourly_rate_entry.get())
                working_hours = Decimal(self.working_hours_entry.get())
                employee.hourly_rate = hourly_rate
                Employee.update_hourly_rate(employee.employee_id, hourly_rate)
                base_salary = hourly_rate * working_hours

            elif employee.type == "commission":
                total_sales = Decimal(self.sales_entry.get())
                commission_rate = Decimal(employee.commission_rate)
                base_salary = commission_rate * total_sales

            strategy = employee.determine_strategy()
            payroll = Payroll(
                employee_id=employee.employee_id,
                base_salary=float(base_salary),
                bonus=float(bonus),
                deductions=float(deductions),
                strategy=strategy
            )

            existing_payroll = Payroll.fetch_by_employee_id(employee.employee_id)
            if existing_payroll:
                self.result_label.config(text=f"Payroll already exists for {employee_name}.", fg="red")
                return

            net_pay = payroll.net_pay
            Payroll.add_payroll_record(employee.employee_id, float(base_salary), float(bonus), float(deductions))
            self.result_label.config(text=f"Net Pay for {employee_name}: {net_pay:.2f}", fg="green")
            self.update_payroll_table()
        except ValueError:
            self.result_label.config(text="Please enter valid numerical values.", fg="red")
        except Exception as e:
            print(f"Error saving payroll record: {e}")
            self.result_label.config(text="An error occurred while saving payroll.", fg="red")

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

    def create_payroll_table(self):
        """
        Create a table to display all payroll records with a scrollbar.
        """
        table_frame = tk.Frame(self)
        table_frame.pack(pady=20, fill="both", expand=True)

        columns = ("Employee Name", "Department", "Base Salary", "Bonus", "Deductions", "Net Pay")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=150)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.update_payroll_table()

    def update_payroll_table(self):
        """
        Update the payroll table with the latest records.
        """
        try:
            for row in self.table.get_children():
                self.table.delete(row)

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

    def go_back(self):
        """
        Navigate back to the previous screen.
        """
        self.app.go_back()
