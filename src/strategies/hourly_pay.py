from src.strategies.payroll_strategy import PayrollStrategy

class HourlyPayStrategy(PayrollStrategy):
    """
    Strategy for calculating pay based on hours worked.
    """
    def __init__(self, hourly_rate, hours_worked):
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked

    def calculate_pay(self, base_salary=0, bonus=0, deductions=0):
        """
        Calculates pay based on hourly rate and hours worked.
        :return: Total calculated pay.
        """
        return (self.hourly_rate * self.hours_worked) + bonus - deductions
