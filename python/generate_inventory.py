"""
=========================================================
PrimeMart FMCG Analytics Platform
Fact Generator: Inventory

Description
-----------
Generates the Inventory Fact Table for the
PrimeMart Enterprise Data Warehouse.

The table represents inventory snapshots
derived from purchases and sales.

Author: David Ezechinyere
=========================================================
"""

from __future__ import annotations

import random

import pandas as pd

from config import GENERATED_DATA

from utils import (
    export_dataframe,
    generation_summary,
    timer,
)

from dimensions import DimensionLoader
# =========================================================
# Inventory Generator
# =========================================================

class InventoryGenerator:
    """
    Generates the FactInventory table.
    """

    def __init__(self):

        loader = DimensionLoader()

        self.products = loader.products

        self.stores = loader.stores

        self.dates = loader.dates

        self.purchases = pd.read_csv(
            GENERATED_DATA / "FactPurchases.csv"
        )

        self.sales = pd.read_csv(
            GENERATED_DATA / "FactSales.csv"
        )

    def generate(self) -> pd.DataFrame:
        """
        Generate the inventory fact table.
        """

        records = []

        latest_date = (
            self.dates["DateKey"].max()
        )

        products = self.products.set_index(
            "ProductID"
        )

        purchase_summary = (
            self.purchases
            .groupby("ProductID")["QuantityPurchased"]
            .sum()
        )

        sales_summary = (
            self.sales
            .groupby("ProductID")["QuantitySold"]
            .sum()
        )

        store_ids = (
            self.stores["StoreID"]
            .tolist()
        )
        inventory_number = 1

        for product_id, product in products.iterrows():

            purchased_qty = int(
                purchase_summary.get(
                    product_id,
                    0,
                )
            )

            sold_qty = int(
                sales_summary.get(
                    product_id,
                    0,
                )
            )

            opening_stock = random.randint(
                200,
                600,
            )

            closing_stock = max(
                opening_stock
                + purchased_qty
                - sold_qty,
                0,
            )

            inventory_value = round(
                closing_stock
                * float(product["UnitCost"]),
                2,
            )
            reorder_level = int(
                product["ReorderLevel"]
            )

            safety_stock = int(
                product["SafetyStock"]
            )
            if closing_stock == 0:

                stock_status = "Out of Stock"

            elif closing_stock <= reorder_level:

                stock_status = "Low Stock"

            elif closing_stock > (
                reorder_level * 3
            ):

                stock_status = "Overstock"

            else:

                stock_status = "Normal"

            for store_id in store_ids:

                records.append(

                    {

                        "InventoryID":
                        f"INV{inventory_number:08d}",

                        "DateKey":
                        latest_date,

                        "StoreID":
                        store_id,

                        "ProductID":
                        product_id,

                        "OpeningStock":
                        opening_stock,

                        "PurchasedQty":
                        purchased_qty,

                        "SoldQty":
                        sold_qty,

                        "ClosingStock":
                        closing_stock,

                        "UnitCost":
                        float(product["UnitCost"]),

                        "InventoryValue":
                        inventory_value,

                        "ReorderLevel":
                        reorder_level,

                        "SafetyStock":
                        safety_stock,

                        "StockStatus":
                        stock_status,

                    }

                )

                inventory_number += 1

        df = pd.DataFrame(records)

        return df

    def validate(
        self,
        df: pd.DataFrame,
    ) -> None:
        """
        Validate inventory data.
        """

        pass


    @timer
    def run(self) -> pd.DataFrame:

        df = self.generate()

        self.validate(df)

        export_dataframe(
            df=df,
            filepath=GENERATED_DATA / "FactInventory.csv",
        )

        generation_summary(
            df=df,
            table_name="FactInventory",
        )

        return df
    # =========================================================
# Main
# =========================================================

def main() -> None:

    InventoryGenerator().run()


if __name__ == "__main__":

    main()