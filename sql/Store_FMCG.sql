USE PrimeMartDW;
GO

CREATE TABLE dbo.DimStore
(
    StoreID CHAR(9) NOT NULL PRIMARY KEY,

    StoreCode CHAR(9) NOT NULL,

    StoreName VARCHAR(100) NOT NULL,

    StoreType VARCHAR(30) NOT NULL,

    State VARCHAR(30) NOT NULL,

    City VARCHAR(50) NOT NULL,

    Address VARCHAR(200) NOT NULL,

    OpeningDate DATE NOT NULL,

    StoreSize VARCHAR(20) NOT NULL,

    FloorAreaSqm INT NOT NULL,

    WarehouseCapacity INT NOT NULL,

    EmployeeCapacity SMALLINT NOT NULL,

    AnnualSalesTarget DECIMAL(18,2) NOT NULL,

    ContactPhone VARCHAR(15) NOT NULL,

    Email VARCHAR(100) NOT NULL,

    ManagerName VARCHAR(100) NOT NULL,

    OperatingHours VARCHAR(30) NOT NULL,

    Status VARCHAR(20) NOT NULL
);
GO