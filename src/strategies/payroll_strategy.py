from abc import ABC, abstractmethod

class PayrollStrategy(ABC):
    """
    Abstract base class for payroll calculation strategies.
    """
    @abstractmethod
    def calculate_pay(self, base_salary, bonus=0, deductions=0):
        pass

class SalaryPayStrategy(PayrollStrategy):
    """
    Strategy for calculating pay for salaried employees.
    """
    def calculate_pay(self, base_salary, bonus=0, deductions=0):
        return base_salary + bonus - deductions

class HourlyPayStrategy(PayrollStrategy):
    """
    Strategy for calculating pay for hourly employees.
    """
    def __init__(self, hourly_rate, hours_worked):
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked

    def calculate_pay(self, base_salary=0, bonus=0, deductions=0):
        return (self.hourly_rate * self.hours_worked) + bonus - deductions

class CommissionPayStrategy(PayrollStrategy):
    """
    Strategy for calculating pay for commission-based employees.
    """
    def __init__(self, commission_rate, total_sales):
        self.commission_rate = commission_rate
        self.total_sales = total_sales

    def calculate_pay(self, base_salary=0, bonus=0, deductions=0):
        return (self.total_sales * self.commission_rate) + bonus - deductions
