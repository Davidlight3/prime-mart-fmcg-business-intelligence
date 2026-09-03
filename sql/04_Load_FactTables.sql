/*============================================================
PrimeMart Enterprise Data Warehouse

Script Name : 04_Load_FactTables.sql
Author      : David Ezechinyere
Purpose     : Load all Fact Tables

Fact Tables
------------
1. FactPurchases
2. FactSales
3. FactInventory
============================================================*/

USE PrimeMartDW;
GO


------------------------------------------------------------
-- FactPurchases
------------------------------------------------------------

TRUNCATE TABLE dbo.FactPurchases;
GO

BULK INSERT dbo.FactPurchases
FROM 'C:\Users\DELL\Desktop\Primemart_FMCG_Analytics\02_Generated_Data\FactPurchases.csv'
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
-- FactSales
------------------------------------------------------------

TRUNCATE TABLE dbo.FactSales;
GO

BULK INSERT dbo.FactSales
FROM 'C:\Users\DELL\Desktop\Primemart_FMCG_Analytics\02_Generated_Data\FactSales.csv'
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
-- FactInventory
------------------------------------------------------------

TRUNCATE TABLE dbo.FactInventory;
GO

BULK INSERT dbo.FactInventory
FROM 'C:\Users\DELL\Desktop\Primemart_FMCG_Analytics\02_Generated_Data\FactInventory.csv'
WITH
(
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0D0A',
    TABLOCK
);
GO


/*============================================================
Verify Fact Table Loads
============================================================*/

SELECT 'FactPurchases' AS TableName,
COUNT(*) AS TotalRows
FROM dbo.FactPurchases

UNION ALL

SELECT 'FactSales',
COUNT(*)
FROM dbo.FactSales

UNION ALL

SELECT 'FactInventory',
COUNT(*)
FROM dbo.FactInventory;
GO