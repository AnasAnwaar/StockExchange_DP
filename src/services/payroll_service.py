from src.strategies.payroll_strategy import PayrollStrategy
from src.strategies.hourly_pay import HourlyPayStrategy
from src.strategies.salary_pay import SalaryPayStrategy
from src.strategies.commission_pay import CommissionPayStrategy


class PayrollService:
    def __init__(self, strategy: PayrollStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: PayrollStrategy):
        self.strategy = strategy

    def calculate_pay(self, base_salary, bonus=0, deductions=0):
        return self.strategy.calculate_pay(base_salary, bonus, deductions)
