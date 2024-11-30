CREATE DATABASE EmployeeERP;
GO

USE EmployeeERP;
GO


CREATE TABLE Employee (
    EmployeeID NVARCHAR(50) PRIMARY KEY, -- Custom Employee ID format
    Name NVARCHAR(100) NOT NULL,
    Email NVARCHAR(100) UNIQUE NOT NULL,
    Phone NVARCHAR(15) NOT NULL,
    Address NVARCHAR(255) NOT NULL,
    Department NVARCHAR(50) NOT NULL,
    Designation NVARCHAR(50) NOT NULL,
    DateOfJoining DATE NOT NULL
);


CREATE TABLE Equipment (
    EquipmentID INT IDENTITY(1,1) PRIMARY KEY,
    Type NVARCHAR(50) NOT NULL,
    Brand NVARCHAR(50) NOT NULL,
    SerialNumber NVARCHAR(50) UNIQUE NOT NULL,
    Status NVARCHAR(20) CHECK (Status IN ('Available', 'Assigned', 'Under Maintenance')) NOT NULL DEFAULT 'Available'
);


CREATE TABLE EquipmentAssignment (
    AssignmentID INT IDENTITY(1,1) PRIMARY KEY,
    EquipmentID INT NOT NULL FOREIGN KEY REFERENCES Equipment(EquipmentID),
    EmployeeID NVARCHAR(50) NOT NULL FOREIGN KEY REFERENCES Employee(EmployeeID),
    AssignedDate DATE NOT NULL,
    ReturnedDate DATE NULL
);

CREATE TABLE Payroll (
    PayrollID INT IDENTITY(1,1) PRIMARY KEY,
    EmployeeID NVARCHAR(50) NOT NULL FOREIGN KEY REFERENCES Employee(EmployeeID),
    BaseSalary DECIMAL(10,2) NOT NULL,
    Bonus DECIMAL(10,2) DEFAULT 0,
    Deductions DECIMAL(10,2) DEFAULT 0,
    NetPay AS (BaseSalary + Bonus - Deductions) PERSISTED
);

CREATE TRIGGER trg_GenerateEmployeeID
ON Employee
INSTEAD OF INSERT
AS
BEGIN
    DECLARE @Department NVARCHAR(50), @NewID NVARCHAR(50);
    DECLARE @MaxID INT;

    SELECT @Department = Department FROM inserted;

    -- Extract the numeric part of the EmployeeID and find the max for the given department
    SELECT @MaxID = ISNULL(MAX(CAST(SUBSTRING(EmployeeID, CHARINDEX('--', EmployeeID) + 2, LEN(EmployeeID)) AS INT)), 0)
    FROM Employee
    WHERE Department = @Department;

    -- Generate the new EmployeeID
    SET @NewID = CONCAT(@Department, '--', FORMAT(@MaxID + 1, '000'));

    -- Insert the new record with the generated EmployeeID
    INSERT INTO Employee (EmployeeID, Name, Email, Phone, Address, Department, Designation, DateOfJoining)
    SELECT @NewID, Name, Email, Phone, Address, Department, Designation, DateOfJoining
    FROM inserted;
END;


INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('John Doe', 'john.doe@example.com', '1234567890', '123 Main St', 'HR', 'Developer', '2023-01-01');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Jane Smith', 'jane.smith@example.com', '0987654321', '456 Elm St', 'IT', 'Manager', '2022-12-15');

SELECT * FROM Employee;


INSERT INTO Equipment (Type, Brand, SerialNumber, Status)
VALUES ('Laptop', 'HP', 'LP-HP-001', 'Available'),
       ('Monitor', 'Dell', 'LED-Dell-002', 'Available');

INSERT INTO EquipmentAssignment (EquipmentID, EmployeeID, AssignedDate)
VALUES (1, 'HR--001', GETDATE()), -- Assign HP Laptop to John Doe
       (2, 'IT--001', GETDATE()); -- Assign Dell Monitor to Jane Smith


INSERT INTO Payroll (EmployeeID, BaseSalary, Bonus, Deductions)
VALUES ('HR--001', 60000, 5000, 2000), -- John Doe's Payroll
       ('IT--001', 80000, 10000, 3000); -- Jane Smith's Payroll

SELECT * FROM Equipment;
SELECT * FROM EquipmentAssignment;
SELECT * FROM Employee;
SELECT * FROM Payroll;

