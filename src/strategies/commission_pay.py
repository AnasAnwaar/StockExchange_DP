from src.strategies.payroll_strategy import PayrollStrategy

class CommissionPayStrategy(PayrollStrategy):
    """
    Strategy for calculating pay for commission-based employees.
    """
    def __init__(self, commission_rate, total_sales):
        self.commission_rate = commission_rate
        self.total_sales = total_sales

    def calculate_pay(self, base_salary=0, bonus=0, deductions=0):
        """
        Calculates pay based on sales and commission rate.
        :return: Total calculated pay.
        """
        return (self.total_sales * self.commission_rate) + bonus - deductions
