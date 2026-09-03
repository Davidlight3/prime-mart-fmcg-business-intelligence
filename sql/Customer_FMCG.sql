USE PrimeMartDW;
GO

CREATE TABLE dbo.DimCustomer
(
    CustomerID CHAR(9) NOT NULL PRIMARY KEY,

    CustomerCode CHAR(10) NOT NULL,

    FirstName VARCHAR(50) NOT NULL,

    LastName VARCHAR(50) NOT NULL,

    Gender VARCHAR(10) NOT NULL,

    DateOfBirth DATE NOT NULL,

    Age TINYINT NOT NULL,

    Email VARCHAR(100) NOT NULL,

    Phone VARCHAR(15) NOT NULL,

    State VARCHAR(30) NOT NULL,

    City VARCHAR(50) NOT NULL,

    CustomerSegment VARCHAR(20) NOT NULL,

    RegistrationDate DATE NOT NULL,

    LoyaltyPoints INT NOT NULL,

    PreferredPaymentMethod VARCHAR(20) NOT NULL,

    LifetimeValue DECIMAL(18,2) NOT NULL,

    Status VARCHAR(20) NOT NULL
);
GO