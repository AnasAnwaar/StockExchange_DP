import tkinter as tk
from src.services.payroll_service import PayrollService
from src.strategies.hourly_pay import HourlyPayStrategy
from src.strategies.salary_pay import SalaryPayStrategy
from src.models.payroll import Payroll


class PayrollScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.service = PayrollService(strategy=SalaryPayStrategy())  # Default strategy

        tk.Label(self, text="Payroll Module", font=("Arial", 30)).pack(pady=20)

        # Employee ID Input
        tk.Label(self, text="Employee ID:").pack()
        self.employee_id_entry = tk.Entry(self)
        self.employee_id_entry.pack()

        # Base Salary Input
        tk.Label(self, text="Base Salary:").pack()
        self.base_salary_entry = tk.Entry(self)
        self.base_salary_entry.pack()

        # Bonus Input
        tk.Label(self, text="Bonus:").pack()
        self.bonus_entry = tk.Entry(self)
        self.bonus_entry.pack()

        # Deductions Input
        tk.Label(self, text="Deductions:").pack()
        self.deductions_entry = tk.Entry(self)
        self.deductions_entry.pack()

        # Calculate Button
        tk.Button(self, text="Calculate Pay", command=self.calculate_pay).pack(pady=10)

        # Result Label
        self.result_label = tk.Label(self, text="")
        self.result_label.pack()

    def calculate_pay(self):
        employee_id = self.employee_id_entry.get()
        base_salary = float(self.base_salary_entry.get())
        bonus = float(self.bonus_entry.get())
        deductions = float(self.deductions_entry.get())

        # Calculate Pay
        net_pay = self.service.calculate_pay(base_salary, bonus, deductions)

        # Show Result
        self.result_label.config(text=f"Net Pay: {net_pay:.2f}")

        # Save Payroll Record to Database
        Payroll.add_payroll_record(employee_id, base_salary, bonus, deductions)
