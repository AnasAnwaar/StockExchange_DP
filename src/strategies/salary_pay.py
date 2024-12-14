from src.strategies.payroll_strategy import PayrollStrategy

class SalaryPayStrategy(PayrollStrategy):
    """
    Strategy for calculating pay for salaried employees.
    """
    def calculate_pay(self, base_salary, bonus=0, deductions=0):
        """
        Calculates pay for salaried employees.
        :return: Total calculated pay.
        """
        return base_salary + bonus - deductions
