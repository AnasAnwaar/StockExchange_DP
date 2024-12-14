import tkinter as tk
from src.ui.employee_ui import EmployeeScreen
from src.ui.payroll_ui import PayrollScreen  # Import the PayrollScreen


class Dashboard(tk.Frame):
    """
    Dashboard screen with navigation to different modules.
    """
    def __init__(self, parent, app):
        """
        Initializes the Dashboard screen.
        :param parent: Parent container for this screen.
        :param app: Reference to the main Application class.
        """
        super().__init__(parent)
        self.app = app  # Reference to the main application

        # Title
        tk.Label(self, text="ERP System Dashboard", font=("Arial", 30)).pack(pady=50)

        # Employee Module Button
        tk.Button(self, text="Employee Module", font=("Arial", 20),
                  command=lambda: self.app.show_screen(EmployeeScreen)).pack(pady=20)

        # Payroll Module Button
        tk.Button(self, text="Payroll Module", font=("Arial", 20),
                  command=lambda: self.app.show_screen(PayrollScreen)).pack(pady=20)

        # Placeholder for other module buttons (e.g., Equipment)
        tk.Button(self, text="Equipment Module (Coming Soon)", font=("Arial", 20), state="disabled").pack(pady=10)

        # Back Button (optional, doesn't navigate anywhere on Dashboard)
        tk.Button(self, text="Back", font=("Arial", 20),
                  command=self.app.go_back).pack(pady=20)

        # Exit Button
        tk.Button(self, text="Exit", font=("Arial", 20),
                  command=self.app.quit).pack(pady=20)
