USE PrimeMartDW;
GO

CREATE TABLE dbo.DimDate
(
    DateKey INT NOT NULL PRIMARY KEY,

    FullDate DATE NOT NULL,

    Day TINYINT NOT NULL,

    DayName VARCHAR(10) NOT NULL,

    DayOfWeek TINYINT NOT NULL,

    WeekOfYear TINYINT NOT NULL,

    Month TINYINT NOT NULL,

    MonthName VARCHAR(15) NOT NULL,

    MonthYear VARCHAR(10) NOT NULL,

    YearMonth CHAR(7) NOT NULL,

    Quarter CHAR(2) NOT NULL,

    Year SMALLINT NOT NULL,

    FiscalMonth TINYINT NOT NULL,

    FiscalQuarter CHAR(2) NOT NULL,

    FiscalYear SMALLINT NOT NULL,

    IsWeekend BIT NOT NULL,

    IsMonthEnd BIT NOT NULL,

    IsQuarterEnd BIT NOT NULL,

    IsYearEnd BIT NOT NULL
);
GO