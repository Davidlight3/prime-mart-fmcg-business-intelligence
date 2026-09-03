"""
=========================================================
PrimeMart FMCG Analytics Platform
Supplier Dimension Generator
=========================================================

Generates the Supplier Dimension table for the
PrimeMart Enterprise Data Warehouse.
"""

from __future__ import annotations

import random
from datetime import timedelta

import pandas as pd
from faker import Faker

from config import GENERATED_DATA, NUM_SUPPLIERS

from constants import (
    SUPPLIER_NAMES,
    SUPPLIER_SUFFIXES,
    PRODUCT_CATEGORIES,
    PAYMENT_TERMS,
    NIGERIAN_STATES,
    
)

from utils import (
    generate_id,
    generate_phone,
    generate_email,
    random_date,
    random_rating,
    random_status,
    generate_category,
    generate_location,
    export_dataframe,
    validate_dataframe,
    generation_summary,
    timer,
)

fake = Faker()


@timer
def generate_suppliers() -> pd.DataFrame:
    """
    Generate Supplier Dimension.
    """

    suppliers = []

    real_supplier_count = len(SUPPLIER_NAMES)

    for i in range(1, NUM_SUPPLIERS + 1):

        supplier_id = generate_id("SUP", i)

        supplier_code = f"SUP-{i:05d}"

        # -----------------------------
        # Supplier Name
        # -----------------------------

        if i <= real_supplier_count:

            supplier_name = SUPPLIER_NAMES[i - 1]

        else:

            supplier_name = (
                fake.company()
                + " "
                + random.choice(SUPPLIER_SUFFIXES)
            )

        # -----------------------------
        # Contact Person
        # -----------------------------

        contact = fake.name()

        # -----------------------------
        # Contact Details
        # -----------------------------

        email = generate_email(contact)

        phone = generate_phone()

       # -----------------------------
       # Location
       # -----------------------------

        state, city = generate_location(NIGERIAN_STATES)

        # -----------------------------
        # Category
        # -----------------------------

        category, subcategory = generate_category(PRODUCT_CATEGORIES)
        # -----------------------------
        # Rating
        # -----------------------------

        rating = random_rating()

        # -----------------------------
        # Payment Terms
        # -----------------------------

        payment_term = random.choice(PAYMENT_TERMS)

        # -----------------------------
        # Lead Time
        # -----------------------------

        lead_time = random.randint(2, 30)

        # -----------------------------
        # Preferred Supplier
        # -----------------------------

        preferred = random.choices(
            ["Yes", "No"],
            weights=[20, 80]
        )[0]

        # -----------------------------
        # Credit Limit
        # -----------------------------

        credit_limit = round(
            random.uniform(
                500000,
                50000000
            ),
            2
        )

        # -----------------------------
        # Status
        # -----------------------------

        status = random_status(92)

        # -----------------------------
        # Contract Dates
        # -----------------------------

        start_date = random_date(
            start_year=2019,
            end_year=2025
        )

        years = random.randint(1, 5)

        end_date = start_date + timedelta(
            days=365 * years
        )

        suppliers.append(
            {
                "SupplierID": supplier_id,
                "SupplierCode": supplier_code,
                "SupplierName": supplier_name,
                "ContactPerson": contact,
                "Email": email,
                "Phone": phone,
                "State": state,
                "City": city,
                "CategorySupplied": category,
                "SupplierRating": rating,
                "PaymentTerms": payment_term,
                "LeadTimeDays": lead_time,
                "PreferredSupplier": preferred,
                "CreditLimit": credit_limit,
                "Status": status,
                "ContractStartDate": start_date.date(),
                "ContractEndDate": end_date.date(),
            }
        )

    df = pd.DataFrame(suppliers)

    validate_dataframe(
        df,
        id_column="SupplierID",
        unique_columns=[
            "SupplierID",
            "SupplierCode",
        ],
        required_columns=[
            "SupplierName",
            "ContactPerson",
            "Email",
            "Phone",
            "CategorySupplied",
        ],
    )

    export_dataframe(
        df,
        GENERATED_DATA / "DimSupplier.csv",
    )

    generation_summary(
        "DimSupplier",
        df,
    )

    return df


if __name__ == "__main__":

    generate_suppliers()