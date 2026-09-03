"""
=========================================================
PrimeMart FMCG Analytics Platform

Date Dimension Generator
=========================================================

Generates the Date Dimension (DimDate)
for the Enterprise Data Warehouse.
"""

from __future__ import annotations

import pandas as pd

from config import (
    GENERATED_DATA,
    DATE_START,
    DATE_END,
)

from utils import (
    export_dataframe,
    validate_dataframe,
    generation_summary,
    timer,
)

# ==========================================================
# Generate Date Dimension
# ==========================================================

@timer
def generate_dates() -> pd.DataFrame:
    """
    Generate the Date Dimension.
    """

    # ------------------------------------------------------
    # Generate Every Date
    # ------------------------------------------------------

    dates = pd.date_range(
        start=DATE_START,
        end=DATE_END,
        freq="D"
    )

    df = pd.DataFrame({

        "FullDate": dates

    })

    # ------------------------------------------------------
    # Primary Key
    # ------------------------------------------------------

    df["DateKey"] = (
        df["FullDate"]
        .dt.strftime("%Y%m%d")
        .astype(int)
    )

    # ------------------------------------------------------
    # Calendar Components
    # ------------------------------------------------------

    df["Day"] = df["FullDate"].dt.day

    df["DayName"] = df["FullDate"].dt.day_name()

    df["DayOfWeek"] = (
        df["FullDate"].dt.dayofweek + 1
    )

    df["WeekOfYear"] = (
        df["FullDate"]
        .dt.isocalendar()
        .week
        .astype(int)
    )

    df["Month"] = df["FullDate"].dt.month

    df["MonthName"] = (
        df["FullDate"].dt.month_name()
    )

    df["Quarter"] = (
        "Q" +
        df["FullDate"]
        .dt.quarter
        .astype(str)
    )

    df["Year"] = df["FullDate"].dt.year

    # ------------------------------------------------------
    # Reporting Columns
    # ------------------------------------------------------

    df["MonthYear"] = (
        df["FullDate"]
        .dt.strftime("%b-%Y")
    )

    df["YearMonth"] = (
        df["FullDate"]
        .dt.strftime("%Y-%m")
    )

    # ------------------------------------------------------
    # Fiscal Calendar
    # (Fiscal Year = Calendar Year)
    # ------------------------------------------------------

    df["FiscalMonth"] = df["Month"]

    df["FiscalQuarter"] = df["Quarter"]

    df["FiscalYear"] = df["Year"]

    # ------------------------------------------------------
# Boolean Flags
# ------------------------------------------------------

    df["IsWeekend"] = (
    (df["DayOfWeek"] >= 6)
    .astype(int)
)

    df["IsMonthEnd"] = (
    df["FullDate"]
    .dt.is_month_end
    .astype(int)
)

    df["IsQuarterEnd"] = (
    df["FullDate"]
    .dt.is_quarter_end
    .astype(int)
)

    df["IsYearEnd"] = (
    df["FullDate"]
    .dt.is_year_end
    .astype(int)
)
    # ------------------------------------------------------
    # Column Order
    # ------------------------------------------------------

    df = df[[
        "DateKey",
        "FullDate",
        "Day",
        "DayName",
        "DayOfWeek",
        "WeekOfYear",
        "Month",
        "MonthName",
        "MonthYear",
        "YearMonth",
        "Quarter",
        "Year",
        "FiscalMonth",
        "FiscalQuarter",
        "FiscalYear",
        "IsWeekend",
        "IsMonthEnd",
        "IsQuarterEnd",
        "IsYearEnd",
    ]]

        # ==========================================================
    # Validate Date Dimension
    # ==========================================================

    validate_dataframe(
        df=df,
        id_column="DateKey",
        unique_columns=[
            "DateKey",
            "FullDate"
        ],
        required_columns=[
            "DateKey",
            "FullDate",
            "MonthName",
            "Quarter",
            "Year"
        ]
    )

    # ==========================================================
    # Export
    # ==========================================================

    export_dataframe(
        df,
        GENERATED_DATA / "DimDate.csv"
    )

    # ==========================================================
    # Summary
    # ==========================================================

    generation_summary(
        df=df,
        table_name="DimDate"
    )

    return df


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    generate_dates()