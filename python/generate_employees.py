"""
=========================================================
PrimeMart FMCG Analytics Platform

Employee Dimension Generator
=========================================================

Generates the Employee Dimension (DimEmployee)
for the Enterprise Data Warehouse.
"""

from __future__ import annotations

import random

import pandas as pd
from faker import Faker

from config import (
    GENERATED_DATA,
)

from constants import (
    JOB_PROFILES,
)

from utils import (
    generate_id,
    generate_phone,
    generate_email,
    random_date,
    random_status,
    export_dataframe,
    validate_dataframe,
    generation_summary,
    timer,
)

fake = Faker()

# ==========================================================
# Load Stores
# ==========================================================

def load_stores() -> pd.DataFrame:
    """
    Load the Store Dimension.
    """

    filepath = GENERATED_DATA / "DimStore.csv"

    return pd.read_csv(filepath)
# ==========================================================
# Employee Allocation
# ==========================================================

def employee_count(store_type: str) -> int:
    """
    Determine employee count
    based on store type.
    """

    if store_type == "Express":
        return random.randint(10, 20)

    elif store_type == "Supermarket":
        return random.randint(25, 60)

    elif store_type == "Hypermarket":
        return random.randint(70, 140)

    else:
        return random.randint(120, 220)

    # ==========================================================
# Mandatory Positions
# ==========================================================

MANDATORY_POSITIONS = [

    "Store Manager",

    "Assistant Manager",

    "Finance Officer",

    "Inventory Officer",

    "Procurement Officer",

    "HR Officer",

    "IT Support",

    "Customer Service Officer",

]

OPERATIONAL_POSITIONS = [

    "Cashier",

    "Sales Associate",

    "Warehouse Officer",

    "Security Officer",

    "Cleaner",

]

# ==========================================================
# Generate Employee Dimension
# ==========================================================

@timer
def generate_employees() -> pd.DataFrame:
    """
    Generate the Employee Dimension.
    """

    stores = load_stores()

    employees = []

    employee_counter = 1

    # ------------------------------------------------------
    # Process One Store At A Time
    # ------------------------------------------------------

    for _, store in stores.iterrows():

        store_id = store["StoreID"]

        store_type = store["StoreType"]

        total_employees = employee_count(store_type)

        # ------------------------------------------
        # Store Manager
        # ------------------------------------------

        manager_id = generate_id("EMP", employee_counter)

        manager_first = fake.first_name()

        manager_last = fake.last_name()

        profile = JOB_PROFILES["Store Manager"]

        employees.append({

            "EmployeeID": manager_id,

            "EmployeeCode": f"EMP{employee_counter:05d}",

            "StoreID": store_id,

            "FirstName": manager_first,

            "LastName": manager_last,

            "Gender": random.choice(["Male", "Female"]),

            "JobTitle": "Store Manager",

            "Department": profile["Department"],

            "HireDate": random_date(
                start_year=2016,
                end_year=2025
            ),

            "EmploymentType": "Full-Time",

            "MonthlySalary": random.randint(
                profile["Salary"][0],
                profile["Salary"][1]
            ),

            "Phone": generate_phone(),

            "Email": generate_email(
                manager_first,
                manager_last
            ),

            "ReportsToEmployeeID": None,

            "Status": random_status(98)

        })

        employee_counter += 1

        assistant_manager_id = None

        # --------------------------------------------------
        # Mandatory Positions
        # --------------------------------------------------

        for position in MANDATORY_POSITIONS:

            if position == "Store Manager":
                continue

            first = fake.first_name()

            last = fake.last_name()

            profile = JOB_PROFILES[position]

            employee_id = generate_id(
                "EMP",
                employee_counter
            )

            if position == "Assistant Manager":
                assistant_manager_id = employee_id

            employees.append({

                "EmployeeID": employee_id,

                "EmployeeCode": f"EMP{employee_counter:05d}",

                "StoreID": store_id,

                "FirstName": first,

                "LastName": last,

                "Gender": random.choice(
                    ["Male", "Female"]
                ),

                "JobTitle": position,

                "Department": profile["Department"],

                "HireDate": random_date(
                    start_year=2016,
                    end_year=2025
                ),

                "EmploymentType": "Full-Time",

                "MonthlySalary": random.randint(
                    profile["Salary"][0],
                    profile["Salary"][1]
                ),

                "Phone": generate_phone(),

                "Email": generate_email(
                    first,
                    last
                ),

                "ReportsToEmployeeID": manager_id,

                "Status": random_status(98)

            })

            employee_counter += 1

        # --------------------------------------------------
        # Remaining Operational Staff
        # --------------------------------------------------

        remaining = total_employees - len(MANDATORY_POSITIONS)

        for _ in range(remaining):

            position = random.choice(
                OPERATIONAL_POSITIONS
            )

            first = fake.first_name()

            last = fake.last_name()

            profile = JOB_PROFILES[position]

            employee_id = generate_id(
                "EMP",
                employee_counter
            )

            reports_to = assistant_manager_id

            if reports_to is None:
                reports_to = manager_id

            employment_type = random.choices(

                [
                    "Full-Time",
                    "Part-Time",
                    "Contract"
                ],

                weights=[75, 15, 10],

                k=1

            )[0]

            employees.append({

                "EmployeeID": employee_id,

                "EmployeeCode": f"EMP{employee_counter:05d}",

                "StoreID": store_id,

                "FirstName": first,

                "LastName": last,

                "Gender": random.choice(
                    ["Male", "Female"]
                ),

                "JobTitle": position,

                "Department": profile["Department"],

                "HireDate": random_date(
                    start_year=2016,
                    end_year=2025
                ),

                "EmploymentType": employment_type,

                "MonthlySalary": random.randint(
                    profile["Salary"][0],
                    profile["Salary"][1]
                ),

                "Phone": generate_phone(),

                "Email": generate_email(
                    first,
                    last
                ),

                "ReportsToEmployeeID": reports_to,

                "Status": random_status(98)

            })

            employee_counter += 1

    df = pd.DataFrame(employees)

        # ==========================================================
    # Validate Employee Dimension
    # ==========================================================

    validate_dataframe(
        df=df,
        id_column="EmployeeID",
        unique_columns=[
            "EmployeeID",
            "EmployeeCode"
        ],
        required_columns=[
            "StoreID",
            "FirstName",
            "LastName",
            "JobTitle",
            "Department",
            "Phone",
            "Email"
        ]
    )

    # ==========================================================
    # Referential Integrity Check
    # ==========================================================

    valid_store_ids = set(stores["StoreID"])

    invalid_store_ids = (
        ~df["StoreID"].isin(valid_store_ids)
    ).sum()

    if invalid_store_ids > 0:

        raise ValueError(
            f"{invalid_store_ids} employees "
            "contain invalid StoreID values."
        )

    # ==========================================================
    # Reporting Hierarchy Validation
    # ==========================================================

    valid_employee_ids = set(df["EmployeeID"])

    reports_to = df["ReportsToEmployeeID"].dropna()

    invalid_managers = (
        ~reports_to.isin(valid_employee_ids)
    ).sum()

    if invalid_managers > 0:

        raise ValueError(
            f"{invalid_managers} employees reference "
            "invalid manager IDs."
        )

    # ==========================================================
    # Export
    # ==========================================================

    export_dataframe(
        df,
        GENERATED_DATA / "DimEmployee.csv"
    )

    # ==========================================================
    # Summary
    # ==========================================================

    generation_summary(
        df=df,
        table_name="DimEmployee"
    )

    return df


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    generate_employees()

    