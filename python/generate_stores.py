"""
=========================================================
PrimeMart FMCG Analytics Platform
Store Dimension Generator
=========================================================

Generates the Store Dimension (DimStore)
for the Enterprise Data Warehouse.
"""

from __future__ import annotations

import random

import pandas as pd
from faker import Faker

from config import (
    GENERATED_DATA,
    NUM_STORES,
)

from constants import (
    STORE_TYPES,
    OPERATING_HOURS,
    NIGERIAN_STATES,
)

from utils import (
    generate_id,
    generate_phone,
    generate_email,
    generate_store_name,
    generate_location,
    random_date,
    random_status,
    export_dataframe,
    validate_dataframe,
    generation_summary,
    timer,
)
print(__file__)
print("generate_stores.py is running...")

fake = Faker()


# ==========================================================
# Store Business Rules
# ==========================================================

def store_profile(store_type: str):
    """
    Return realistic store characteristics
    based on the store type.
    """

    if store_type == "Express":

        return (
            "Small",
            random.randint(300, 900),
            random.randint(8, 20),
            random.randint(500, 2000),
            random.randint(
                150_000_000,
                400_000_000
            ),
        )

    elif store_type == "Supermarket":

        return (
            "Medium",
            random.randint(900, 2500),
            random.randint(20, 60),
            random.randint(2000, 10000),
            random.randint(
                500_000_000,
                1_200_000_000
            ),
        )

    elif store_type == "Hypermarket":

        return (
            "Large",
            random.randint(2500, 6000),
            random.randint(60, 150),
            random.randint(10000, 40000),
            random.randint(
                1_500_000_000,
                3_000_000_000
            ),
        )

    else:
        # Warehouse

        return (
            "Warehouse",
            random.randint(5000, 12000),
            random.randint(120, 250),
            random.randint(40000, 100000),
            random.randint(
                3_000_000_000,
                5_000_000_000
            ),
        )

    # ==========================================================
# Generate Store Dimension
# ==========================================================

@timer
def generate_stores() -> pd.DataFrame:
    """
    Generate the Store Dimension.
    """

    stores = []

    store_type_weights = [
        30,   # Express
        40,   # Supermarket
        20,   # Hypermarket
        10    # Warehouse
    ]

    for i in range(1, NUM_STORES + 1):

        # ------------------------------------------
        # Primary Keys
        # ------------------------------------------

        store_id = generate_id("STR", i)

        store_code = f"STORE{i:04d}"

        # ------------------------------------------
        # Store Type
        # ------------------------------------------

        store_type = random.choices(
            STORE_TYPES,
            weights=store_type_weights,
            k=1
        )[0]

        (
            store_size,
            floor_area,
            employee_capacity,
            warehouse_capacity,
            annual_sales_target
        ) = store_profile(store_type)

        # ------------------------------------------
        # Location
        # ------------------------------------------

        state, city = generate_location(
            NIGERIAN_STATES
        )

        address = fake.street_address()

        # ------------------------------------------
        # Store Information
        # ------------------------------------------

        store_name = generate_store_name(city)

        manager_name = fake.name()

        phone = generate_phone()

        email = generate_email(store_name)

        opening_date = random_date(
            start_year=2016,
            end_year=2025
        )

        operating_hours = random.choice(
            OPERATING_HOURS
        )

        status = random_status(
            active_weight=95
        )

        # ------------------------------------------
        # Store Record
        # ------------------------------------------

        store = {

            "StoreID": store_id,

            "StoreCode": store_code,

            "StoreName": store_name,

            "StoreType": store_type,

            "State": state,

            "City": city,

            "Address": address,

            "OpeningDate": opening_date,

            "StoreSize": store_size,

            "FloorAreaSqm": floor_area,

            "WarehouseCapacity": warehouse_capacity,

            "EmployeeCapacity": employee_capacity,

            "AnnualSalesTarget": annual_sales_target,

            "ContactPhone": phone,

            "Email": email,

            "ManagerName": manager_name,

            "OperatingHours": operating_hours,

            "Status": status

        }

        stores.append(store)

    df = pd.DataFrame(stores)

# ==========================================================
# Create DataFrame
# ==========================================================

    # Validate Data
    validate_dataframe(
        df=df,
        id_column="StoreID",
        unique_columns=[
            "StoreID",
            "StoreCode"
        ],
        required_columns=[
            "StoreName",
            "State",
            "City",
            "ManagerName",
            "ContactPhone",
            "Email"
        ]
    )

    # Export CSV
    export_dataframe(
        df,
        GENERATED_DATA / "DimStore.csv"
    )

    # Generation Summary
    generation_summary(
        df=df,
        table_name="DimStore"
    )

    return df


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    generate_stores()