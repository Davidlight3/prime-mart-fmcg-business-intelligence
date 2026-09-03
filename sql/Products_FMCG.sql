USE PrimeMartDW;
GO

CREATE TABLE dbo.DimProduct
(
    ProductID CHAR(9) NOT NULL PRIMARY KEY,

    SKU VARCHAR(20) NOT NULL,

    ProductName VARCHAR(100) NOT NULL,

    Brand VARCHAR(50) NOT NULL,

    Category VARCHAR(50) NOT NULL,

    SubCategory VARCHAR(50) NOT NULL,

    UnitOfMeasure VARCHAR(20) NOT NULL,

    PackageSize VARCHAR(20) NOT NULL,

    UnitCost DECIMAL(18,2) NOT NULL,

    SellingPrice DECIMAL(18,2) NOT NULL,

    ProfitMarginPct DECIMAL(5,2) NOT NULL,

    VATRate DECIMAL(4,2) NOT NULL,

    ReorderLevel INT NOT NULL,

    SafetyStock INT NOT NULL,

    LaunchDate DATE NOT NULL,

    Status VARCHAR(20) NOT NULL
);



EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;

EXEC sp_configure 'Ad Hoc Distributed Queries', 1;
RECONFIGURE;

EXEC xp_cmdshell 'dir "C:\Users\DELL\Desktop\Primemart_FMCG_Analytics\02_Generated_Data"';
GO