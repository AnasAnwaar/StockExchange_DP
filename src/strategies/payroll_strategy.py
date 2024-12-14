from abc import ABC, abstractmethod

class PayrollStrategy(ABC):
    """
    Abstract base class for payroll calculation strategies.
    """

    @abstractmethod
    def calculate_pay(self, base_salary, bonus=0, deductions=0):
        """
        Abstract method to calculate payroll based on a strategy.
        :param base_salary: The base salary of the employee.
        :param bonus: Additional bonuses (default: 0).
        :param deductions: Deductions from the salary (default: 0).
        :return: Calculated pay.
        """
        pass
