import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pyodbc
from modules.employee_management import EmployeeManagement

def connect_to_database():
    """
    Establish connection to the database.
    """
    connection = pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=DESKTOP-HS9F6CR\MSSQLSERVER01;"  
        "DATABASE=EmployeeERP;"
        "Trusted_Connection=yes;"
    )
    return connection

def main():
    # Connect to the database
    connection = connect_to_database()
    employee_manager = EmployeeManagement(connection)

    # Tkinter GUI setup
    root = tk.Tk()
    root.title("Employee ERP System")
    root.geometry("800x600")

    # Frame for the employee display section
    employee_frame = tk.Frame(root)
    employee_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    # Scrollbar and Listbox for displaying employees
    scroll_y = tk.Scrollbar(employee_frame, orient=tk.VERTICAL)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

    employee_listbox = tk.Listbox(employee_frame, selectmode=tk.SINGLE, height=10, width=70, yscrollcommand=scroll_y.set)
    employee_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    scroll_y.config(command=employee_listbox.yview)

    # Frame for employee form (Initially hidden)
    form_frame = tk.Frame(root)

    def display_employees():
        employees = employee_manager.fetch_all_employees()

        # Clear the listbox before inserting new entries
        employee_listbox.delete(0, tk.END)

        # Insert employee data into the listbox
        for employee in employees:
            employee_info = f"{employee.EmployeeID} - {employee.Name} - {employee.Department} - {employee.Designation}"
            employee_listbox.insert(tk.END, employee_info)

    def show_add_employee_form():
        # Hide the employee list and show the form
        employee_frame.pack_forget()

        form_frame.pack(padx=20, pady=20)

        # Create the form fields
        name_label = tk.Label(form_frame, text="Name:")
        name_label.grid(row=0, column=0, padx=10, pady=5)
        name_entry = tk.Entry(form_frame)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        email_label = tk.Label(form_frame, text="Email:")
        email_label.grid(row=1, column=0, padx=10, pady=5)
        email_entry = tk.Entry(form_frame)
        email_entry.grid(row=1, column=1, padx=10, pady=5)

        phone_label = tk.Label(form_frame, text="Phone:")
        phone_label.grid(row=2, column=0, padx=10, pady=5)
        phone_entry = tk.Entry(form_frame)
        phone_entry.grid(row=2, column=1, padx=10, pady=5)

        address_label = tk.Label(form_frame, text="Address:")
        address_label.grid(row=3, column=0, padx=10, pady=5)
        address_entry = tk.Entry(form_frame)
        address_entry.grid(row=3, column=1, padx=10, pady=5)

        department_label = tk.Label(form_frame, text="Department:")
        department_label.grid(row=4, column=0, padx=10, pady=5)
        department_entry = tk.Entry(form_frame)
        department_entry.grid(row=4, column=1, padx=10, pady=5)

        designation_label = tk.Label(form_frame, text="Designation:")
        designation_label.grid(row=5, column=0, padx=10, pady=5)
        designation_entry = tk.Entry(form_frame)
        designation_entry.grid(row=5, column=1, padx=10, pady=5)

        doj_label = tk.Label(form_frame, text="Date of Joining (YYYY-MM-DD):")
        doj_label.grid(row=6, column=0, padx=10, pady=5)
        doj_entry = tk.Entry(form_frame)
        doj_entry.grid(row=6, column=1, padx=10, pady=5)

        def submit_employee():
            # Get data from form entries
            name = name_entry.get()
            email = email_entry.get()
            phone = phone_entry.get()
            address = address_entry.get()
            department = department_entry.get()
            designation = designation_entry.get()
            doj = doj_entry.get()

            # Insert employee into the database
            try:
                employee_manager.add_employee(name, email, phone, address, department, designation, doj)
                messagebox.showinfo("Success", "Employee added successfully!")
                show_employee_list()  # After adding, show the list again
            except Exception as e:
                messagebox.showerror("Error", f"Error adding employee: {e}")

        # Submit button to add employee
        submit_button = ttk.Button(form_frame, text="Submit", command=submit_employee)
        submit_button.grid(row=7, column=0, columnspan=2, pady=20)

    def show_employee_list():
        # Hide the form and show the employee list
        form_frame.pack_forget()
        employee_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        display_employees()

    # Button to fetch employees
    fetch_button = ttk.Button(root, text="Fetch Employees", command=show_employee_list)
    fetch_button.pack(pady=20, side=tk.LEFT, padx=20)

    # Button to add employee
    add_button = ttk.Button(root, text="Add Employee", command=show_add_employee_form)
    add_button.pack(pady=20, side=tk.LEFT)

    # Run the GUI
    root.mainloop()

if __name__ == "__main__":
    main()
