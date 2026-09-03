"""
=========================================================
PrimeMart FMCG Analytics Platform
Dimension Generator: Product

Description
-----------
Generates the Product Dimension (DimProduct)
for the PrimeMart Enterprise Data Warehouse.

Author: David Ezechinyere
=========================================================
"""

from __future__ import annotations

import random

import pandas as pd

from config import (
    GENERATED_DATA,
    NUM_PRODUCTS,
)

from constants import (
    BRANDS,
    PRODUCT_NAMES,
    UNITS,
    PACKAGE_SIZES,
    VAT_RATE,
)

from utils import (
    generate_id,
    generate_prices,
    generate_sku,
    random_date,
    export_dataframe,
    validate_dataframe,
    generation_summary,
    timer,
)


# =========================================================
# Product Generator
# =========================================================

@timer
def generate_products() -> pd.DataFrame:
    """
    Generate the Product Dimension.

    Returns
    -------
    pd.DataFrame
        Product Dimension.
    """

    records = []

    categories = list(PRODUCT_NAMES.keys())

    product_status = [
        "Active",
        "Active",
        "Active",
        "Discontinued",
    ]

    for index in range(1, NUM_PRODUCTS + 1):

        # -------------------------------------------------
        # Product Classification
        # -------------------------------------------------

        category = random.choice(categories)

        subcategory = random.choice(
            PRODUCT_NAMES[category]
        )

        brand = random.choice(BRANDS)

        # -------------------------------------------------
        # Product Identification
        # -------------------------------------------------

        product_id = generate_id(
            prefix="PRD",
            number=index,
        )

        sku = generate_sku(
            brand=brand,
            category=category,
            number=index,
        )

        # -------------------------------------------------
        # Pricing
        # -------------------------------------------------

        unit_cost, selling_price, margin = (
            generate_prices()
        )

        # -------------------------------------------------
        # Product Record
        # -------------------------------------------------

        records.append(

            {

                "ProductID": product_id,

                "SKU": sku,

                "ProductName": f"{brand} {subcategory}",

                "Brand": brand,

                "Category": category,

                "SubCategory": subcategory,

                "UnitOfMeasure": random.choice(
                    UNITS
                ),

                "PackageSize": random.choice(
                    PACKAGE_SIZES
                ),

                "UnitCost": unit_cost,

                "SellingPrice": selling_price,

                "ProfitMarginPct": margin,

                "VATRate": VAT_RATE,

                "ReorderLevel": random.randint(
                    20,
                    120,
                ),

                "SafetyStock": random.randint(
                    10,
                    40,
                ),

                "LaunchDate": random_date(),

                "Status": random.choice(
                    product_status
                ),

            }

        )

    # =====================================================
    # Create DataFrame
    # =====================================================

    df = pd.DataFrame(records)

    # =====================================================
    # Validate Data
    # =====================================================

    validate_dataframe(
        df=df,
        id_column="ProductID",
        unique_columns=[
            "ProductID",
            "SKU",
        ],
        required_columns=[
            "ProductName",
            "Brand",
            "Category",
            "SubCategory",
            "UnitCost",
            "SellingPrice",
            "VATRate",
            "Status",
        ],
    )

    # =====================================================
    # Export CSV
    # =====================================================

    output_file = (
        GENERATED_DATA /
        "DimProduct.csv"
    )

    export_dataframe(
        df=df,
        filepath=output_file,
    )

    # =====================================================
    # Generation Summary
    # =====================================================

    generation_summary(
        df=df,
        table_name="DimProduct",
    )

    return df


# =========================================================
# Main
# =========================================================

if __name__ == "__main__":

    generate_products()