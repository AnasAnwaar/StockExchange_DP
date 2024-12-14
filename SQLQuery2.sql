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







INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Alice Brown', 'alice.brown3@example.com', '1234500003', '789 Oak St', 'Finance', 'Analyst', '2023-06-10');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Bob Johnson', 'bob.johnson4@example.com', '1234500004', '321 Pine St', 'Operations', 'Coordinator', '2021-09-20');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Charlie Green', 'charlie.green5@example.com', '1234500005', '654 Maple St', 'Sales', 'Consultant', '2020-11-05');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('David Clark', 'david.clark6@example.com', '1234500006', '987 Cedar St', 'HR', 'Manager', '2023-03-15');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Eve Adams', 'eve.adams7@example.com', '1234500007', '222 Birch St', 'IT', 'Developer', '2022-08-25');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Frank Moore', 'frank.moore8@example.com', '1234500008', '444 Willow St', 'Finance', 'Analyst', '2021-05-13');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Grace Hall', 'grace.hall9@example.com', '1234500009', '666 Spruce St', 'Operations', 'Coordinator', '2020-12-18');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Henry Baker', 'henry.baker10@example.com', '1234500010', '888 Redwood St', 'Sales', 'Consultant', '2019-10-22');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Ivy Bell', 'ivy.bell11@example.com', '1234500011', '111 Sequoia St', 'HR', 'Analyst', '2023-07-14');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Jack Carter', 'jack.carter12@example.com', '1234500012', '333 Magnolia St', 'IT', 'Manager', '2022-02-10');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Kathy Fisher', 'kathy.fisher13@example.com', '1234500013', '555 Poplar St', 'Finance', 'Coordinator', '2021-04-30');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Leo Harris', 'leo.harris14@example.com', '1234500014', '777 Aspen St', 'Operations', 'Developer', '2020-06-12');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Mia Scott', 'mia.scott15@example.com', '1234500015', '999 Alder St', 'Sales', 'Consultant', '2019-08-25');



SELECT * FROM Employee;
INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Nathan Young', 'nathan.young16@example.com', '1234500016', '345 Cedar Rd', 'HR', 'Manager', '2023-05-11');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Olivia White', 'olivia.white17@example.com', '1234500017', '567 Walnut Ave', 'IT', 'Analyst', '2022-11-07');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Paul Walker', 'paul.walker18@example.com', '1234500018', '789 Spruce Blvd', 'Finance', 'Developer', '2021-04-21');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Quinn Price', 'quinn.price19@example.com', '1234500019', '901 Maple Ln', 'Operations', 'Consultant', '2020-09-15');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Rachel Adams', 'rachel.adams20@example.com', '1234500020', '123 Birch Ct', 'Sales', 'Coordinator', '2019-03-29');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Samuel Brooks', 'samuel.brooks21@example.com', '1234500021', '345 Aspen Way', 'HR', 'Analyst', '2023-06-18');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Tina Black', 'tina.black22@example.com', '1234500022', '567 Redwood Ave', 'IT', 'Manager', '2022-01-25');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Ursula Blake', 'ursula.blake23@example.com', '1234500023', '789 Magnolia St', 'Finance', 'Developer', '2021-08-10');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Victor Lane', 'victor.lane24@example.com', '1234500024', '901 Sequoia Ct', 'Operations', 'Consultant', '2020-05-22');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Wendy Hale', 'wendy.hale25@example.com', '1234500025', '123 Alder St', 'Sales', 'Coordinator', '2019-12-03');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Xavier Cruz', 'xavier.cruz26@example.com', '1234500026', '345 Cedar Rd', 'HR', 'Manager', '2023-02-14');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Yara Stone', 'yara.stone27@example.com', '1234500027', '567 Walnut Ave', 'IT', 'Analyst', '2022-06-30');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Zach King', 'zach.king28@example.com', '1234500028', '789 Spruce Blvd', 'Finance', 'Developer', '2021-10-11');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Anna Collins', 'anna.collins29@example.com', '1234500029', '901 Maple Ln', 'Operations', 'Consultant', '2020-01-17');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Brian Hayes', 'brian.hayes30@example.com', '1234500030', '123 Birch Ct', 'Sales', 'Coordinator', '2019-07-27');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Chloe Rogers', 'chloe.rogers31@example.com', '1234500031', '345 Aspen Way', 'HR', 'Analyst', '2023-03-19');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Daniel Perez', 'daniel.perez32@example.com', '1234500032', '567 Redwood Ave', 'IT', 'Manager', '2022-04-25');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Ella Foster', 'ella.foster33@example.com', '1234500033', '789 Magnolia St', 'Finance', 'Developer', '2021-09-10');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Frank Bell', 'frank.bell34@example.com', '1234500034', '901 Sequoia Ct', 'Operations', 'Consultant', '2020-06-15');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Grace Lewis', 'grace.lewis35@example.com', '1234500035', '123 Alder St', 'Sales', 'Coordinator', '2019-11-23');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Holly Carter', 'holly.carter36@example.com', '1234500036', '345 Cedar Rd', 'HR', 'Manager', '2023-01-12');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Isaac Young', 'isaac.young37@example.com', '1234500037', '567 Walnut Ave', 'IT', 'Analyst', '2022-07-29');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Jacob Long', 'jacob.long38@example.com', '1234500038', '789 Spruce Blvd', 'Finance', 'Developer', '2021-05-19');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Karen Baker', 'karen.baker39@example.com', '1234500039', '901 Maple Ln', 'Operations', 'Consultant', '2020-10-27');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Liam Brooks', 'liam.brooks40@example.com', '1234500040', '123 Birch Ct', 'Sales', 'Coordinator', '2019-08-14');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Molly James', 'molly.james41@example.com', '1234500041', '345 Aspen Way', 'HR', 'Analyst', '2023-04-02');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Noah Wright', 'noah.wright42@example.com', '1234500042', '567 Redwood Ave', 'IT', 'Manager', '2022-02-18');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Olivia Turner', 'olivia.turner43@example.com', '1234500043', '789 Magnolia St', 'Finance', 'Developer', '2021-06-13');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Peter Harris', 'peter.harris44@example.com', '1234500044', '901 Sequoia Ct', 'Operations', 'Consultant', '2020-12-09');

INSERT INTO Employee (Name, Email, Phone, Address, Department, Designation, DateOfJoining)
VALUES ('Quinn Ward', 'quinn.ward45@example.com', '1234500045', '123 Alder St', 'Sales', 'Coordinator', '2019-09-01');
