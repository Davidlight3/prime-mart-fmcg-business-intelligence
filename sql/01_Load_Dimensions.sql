USE PrimeMartDW;
GO

/*==========================================================
  PrimeMart Data Warehouse
  ETL Script - Load Dimension Tables
==========================================================*/

------------------------------------------------------------
-- 1. DimDate
------------------------------------------------------------
TRUNCATE TABLE dbo.DimDate;
GO

BULK INSERT dbo.DimDate
FROM 'C:\Users\DELL\Desktop\Primemart_FMCG_Analytics\02_Generated_Data\DimDate.csv'
WITH
(
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0D0A',
    TABLOCK
);
GO

------------------------------------------------------------
-- 2. DimCustomer
------------------------------------------------------------
TRUNCATE TABLE dbo.DimCustomer;
GO

BULK INSERT dbo.DimCustomer
FROM 'C:\Users\DELL\Desktop\Primemart_FMCG_Analytics\02_Generated_Data\DimCustomer.csv'
WITH
(
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0D0A',
    TABLOCK
);
GO

------------------------------------------------------------
-- 3. DimStore
------------------------------------------------------------
TRUNCATE TABLE dbo.DimStore;
GO

BULK INSERT dbo.DimStore
FROM 'C:\Users\DELL\Desktop\Primemart_FMCG_Analytics\02_Generated_Data\DimStore.csv'
WITH
(
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0D0A',
    TABLOCK
);
GO

------------------------------------------------------------
-- 4. DimSupplier
------------------------------------------------------------
TRUNCATE TABLE dbo.DimSupplier;
GO

BULK INSERT dbo.DimSupplier
FROM 'C:\Users\DELL\Desktop\Primemart_FMCG_Analytics\02_Generated_Data\DimSupplier.csv'
WITH
(
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0D0A',
    TABLOCK
);
GO

------------------------------------------------------------
-- 5. DimProduct
------------------------------------------------------------
TRUNCATE TABLE dbo.DimProduct;
GO

BULK INSERT dbo.DimProduct
FROM 'C:\Users\DELL\Desktop\Primemart_FMCG_Analytics\02_Generated_Data\DimProduct.csv'
WITH
(
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0D0A',
    TABLOCK
);
GO

------------------------------------------------------------
-- 6. DimEmployee
------------------------------------------------------------
TRUNCATE TABLE dbo.DimEmployee;
GO

BULK INSERT dbo.DimEmployee
FROM 'C:\Users\DELL\Desktop\Primemart_FMCG_Analytics\02_Generated_Data\DimEmployee.csv'
WITH
(
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0D0A',
    TABLOCK
);
GO


SELECT COUNT(*) FROM dbo.DimCustomer;

SELECT COUNT(*) FROM dbo.DimStore;

SELECT COUNT(*) FROM dbo.DimSupplier;

SELECT COUNT(*) FROM dbo.DimProduct;

SELECT COUNT(*) FROM dbo.DimEmployee;