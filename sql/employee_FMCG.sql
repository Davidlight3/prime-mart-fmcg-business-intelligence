USE PrimeMartDW;
GO

CREATE TABLE dbo.DimEmployee
(
    EmployeeID CHAR(9) NOT NULL PRIMARY KEY,

    EmployeeCode CHAR(8) NOT NULL,

    StoreID CHAR(9) NOT NULL,

    FirstName VARCHAR(50) NOT NULL,

    LastName VARCHAR(50) NOT NULL,

    Gender VARCHAR(10) NOT NULL,

    JobTitle VARCHAR(50) NOT NULL,

    Department VARCHAR(30) NOT NULL,

    HireDate DATE NOT NULL,

    EmploymentType VARCHAR(20) NOT NULL,

    MonthlySalary DECIMAL(12,2) NOT NULL,

    Phone VARCHAR(15) NOT NULL,

    Email VARCHAR(100) NOT NULL,

    ReportsToEmployeeID CHAR(9) NULL,

    Status VARCHAR(20) NOT NULL
);
GO