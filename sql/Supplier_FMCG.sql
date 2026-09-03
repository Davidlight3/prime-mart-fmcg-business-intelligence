USE PrimeMartDW;
GO

CREATE TABLE dbo.DimSupplier
(
    SupplierID CHAR(9) NOT NULL PRIMARY KEY,

    SupplierCode CHAR(9) NOT NULL,

    SupplierName VARCHAR(100) NOT NULL,

    ContactPerson VARCHAR(100) NOT NULL,

    Email VARCHAR(100) NOT NULL,

    Phone VARCHAR(15) NOT NULL,

    State VARCHAR(30) NOT NULL,

    City VARCHAR(50) NOT NULL,

    CategorySupplied VARCHAR(30) NOT NULL,

    SupplierRating DECIMAL(3,1) NOT NULL,

    PaymentTerms VARCHAR(20) NOT NULL,

    LeadTimeDays SMALLINT NOT NULL,

    PreferredSupplier VARCHAR(3) NOT NULL,

    CreditLimit DECIMAL(18,2) NOT NULL,

    Status VARCHAR(20) NOT NULL,

    ContractStartDate DATE NOT NULL,

    ContractEndDate DATE NOT NULL
);
GO