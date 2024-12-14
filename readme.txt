# Employee ERP System

The **Employee ERP System** is a Python-based desktop application designed for managing employee records, equipment assignments, and payroll. Built using **Tkinter** for the user interface and **Microsoft SQL Server (MSSQL)** for database management, this system incorporates **design patterns** to ensure scalability, maintainability, and flexibility.

---

## Features

### 1. **Employee Management**
- Add, update, delete, and view employee details.
- Generate custom `EmployeeID` in the format `<Department>--<Number>` (e.g., `HR--001`).
- Assign employees to departments and track their designations.

### 2. **Equipment Management**
- Track and manage equipment such as laptops, monitors, and keyboards.
- Assign equipment to employees with due dates and statuses.
- Generate unique serial numbers for equipment using a configurable format.

### 3. **Payroll Management**
- Calculate employee payroll, including base salary, bonuses, and deductions.
- Automatically compute `NetPay` and generate detailed payroll records.
- Prevent duplicate payroll records for the same employee.

### 4. **User-Friendly Interface**
- Interactive Tkinter-based UI for easy navigation and usage.
- Integrated dropdowns, tables with scrollbars, and buttons for a seamless experience.

---

## Design Patterns Used

### **Creational Patterns**
1. **Abstract Factory**: For generating equipment serial numbers dynamically.
2. **Singleton**: Ensures a single instance of the database connection.
3. **Builder**: Constructs employee and payroll objects with multiple attributes.

### **Structural Patterns**
1. **Composite**: Manages groups of employees and their equipment assignments.
2. **Adapter**: Bridges the gap between UI components and backend services.

### **Behavioral Patterns**
1. **Observer**: Sends notifications to employees for equipment assignments and payroll updates.
2. **Strategy**: Enables flexible payroll calculation methods.
3. **Command**: Encapsulates user actions (e.g., button clicks) for modularity.

---

## Requirements

### **Software**
- Python 3.9+ (or above)
- Microsoft SQL Server (MSSQL) with SSMS
- Tkinter (pre-installed with Python)

### **Python Libraries**
Install the required libraries:
```bash
pip install pyodbc
pip install pandas
```

---

## Database Schema

### Tables
1. **Employee**
   - `EmployeeID` (Primary Key): Custom ID in the format `<Department>--<Number>`.
   - `Name`, `Email`, `Phone`, `Address`, `Department`, `Designation`, `DateOfJoining`.

2. **Equipment**
   - `EquipmentID` (Primary Key): Auto-incremented.
   - `Type`, `Brand`, `SerialNumber` (Unique), `Status`.

3. **EquipmentAssignment**
   - `AssignmentID` (Primary Key): Auto-incremented.
   - Foreign Keys: `EquipmentID`, `EmployeeID`.
   - `AssignedDate`, `ReturnedDate`.

4. **Payroll**
   - `PayrollID` (Primary Key): Auto-incremented.
   - Foreign Key: `EmployeeID`.
   - `BaseSalary`, `Bonus`, `Deductions`, `NetPay`.

---

## How to Run

### 1. **Set Up the Database**
- Execute the SQL scripts provided in the `database.sql` file to create and initialize the database.
- Update the database connection details in the `DatabaseHandler` class within `database/handler.py`.

### 2. **Run the Application**
- Launch the application by running the main Python file:
```bash
python main.py
```

---

## Project Structure
```
EmployeeERP/
│
├── main.py                 # Entry point for the application
├── models/
│   ├── employee.py         # Employee class and logic
│   ├── equipment.py        # Equipment class and logic
│   ├── payroll.py          # Payroll class and calculations
│   ├── assignment.py       # EquipmentAssignment logic
│
├── database/
│   ├── handler.py          # DatabaseHandler (Singleton pattern)
│   ├── database.sql        # SQL scripts for schema and initial data
│
├── ui/
│   ├── dashboard_ui.py     # Main dashboard UI
│   ├── employee_ui.py      # Employee management UI
│   ├── payroll_ui.py       # Payroll management UI
│   ├── equipment_ui.py     # Equipment management UI
│
└── utils/
    ├── serial_generator.py # SerialNumberGenerator (Abstract Factory pattern)
    ├── notification.py     # NotificationManager (Observer pattern)
```

---

## Key Features in the Application
1. **Intuitive Navigation**:
   - Modular UI structure for navigating between employees, equipment, and payroll modules.
2. **Error Prevention**:
   - Prevents duplicate payroll records or invalid equipment assignments.
3. **Scalability**:
   - Modular design and use of design patterns enable easy expansion (e.g., adding new modules).

---

## Future Enhancements
1. **Attendance Management**:
   - Record employee attendance and integrate with payroll calculations.

2. **Leave Management**:
   - Add functionality for applying, approving, and tracking employee leaves.

3. **Report Generation**:
   - Export payroll and equipment usage reports in CSV or PDF formats.

4. **Performance Tracking**:
   - Monitor employee performance metrics and generate insights.

5. **Notifications**:
   - Email or in-app notifications for employees regarding assignments, payroll, or updates.

---

## Contributing
We welcome contributions to enhance this project! Follow these steps to contribute:
1. Fork this repository.
2. Make your changes.
3. Submit a pull request with detailed explanations of your updates.

---

### Example Screenshots (Optional)
If possible, add screenshots of the application to provide a visual understanding of its interface and features.
