"""
=========================================================
PrimeMart FMCG Analytics Platform
Fact Table Generator: Sales
=========================================================

Generates the FactSales table for the
PrimeMart Enterprise Data Warehouse.

Author: David Ezechinyere
=========================================================
"""

from __future__ import annotations

from asyncio.log import logger
from py_compile import main
import random
from dataclasses import dataclass
from datetime import datetime, timedelta

import pandas as pd

from config import (
    GENERATED_DATA,
    NUM_SALES,
)

from constants import (
    PAYMENT_METHODS,
    SALES_CHANNELS,
    SALES_STATUS,
    ELIGIBLE_JOB_TITLES,
)

from utils import (
    export_dataframe,
    generation_summary,
    load_dimension,
    timer,
    validate_dataframe,
)
# ==========================================================
# Financial Model
# ==========================================================

@dataclass(slots=True)
class SalesAmounts:

    gross: float

    discount: float

    net: float

    vat: float

    total: float

    cost: float

    profit: float

    margin: float
    # ==========================================================
# Sales Generator
# ==========================================================

class SalesGenerator:

    def __init__(self):

        self.customers = load_dimension("DimCustomer")
        self.products = load_dimension("DimProduct")
        self.stores = load_dimension("DimStore")
        self.employees = load_dimension("DimEmployee")
        self.dates = load_dimension("DimDate")

        self._validate_sources()

    def _require(
        self,
        df: pd.DataFrame,
        name: str,
        required: set[str],
    ) -> None:

        missing = required - set(df.columns)

        if missing:
            raise ValueError(
                f"{name} missing columns: {sorted(missing)}"
            )

    def _validate_sources(self) -> None:

        ...
    def _validate_sources(self) -> None:
        """
        Validate all required source dimensions.
        """

        self._require(
            self.customers,
            "DimCustomer",
            {"CustomerID"},
        )

        self._require(
            self.products,
            "DimProduct",
            {
                "ProductID",
                "SellingPrice",
                "UnitCost",
                "VATRate",
            },
        )

        self._require(
            self.stores,
            "DimStore",
            {"StoreID"},
        )

        self._require(
            self.employees,
            "DimEmployee",
            {
                "EmployeeID",
                "JobTitle",
            },
        )

        self._require(
            self.dates,
            "DimDate",
            {"DateKey"},
        )

    def _amounts(
        self,
        quantity: int,
        selling_price: float,
        unit_cost: float,
        discount_pct: float,
        vat_rate: float,
    ) -> SalesAmounts:
        """
        Calculate all financial metrics for a sales transaction.
        """

        gross = round(
            quantity * selling_price,
            2,
        )

        discount = round(
            gross * discount_pct / 100,
            2,
        )

        net = round(
            gross - discount,
            2,
        )

        vat = round(
            net * vat_rate / 100,
            2,
        )

        total = round(
            net + vat,
            2,
        )

        cost = round(
            quantity * unit_cost,
            2,
        )

        profit = round(
            net - cost,
            2,
        )

        margin = (
            round(
                (profit / net) * 100,
                2,
            )
            if net > 0
            else 0.0
        )

        return SalesAmounts(
            gross=gross,
            discount=discount,
            net=net,
            vat=vat,
            total=total,
            cost=cost,
            profit=profit,
            margin=margin,
        )

    def generate(self) -> pd.DataFrame:
        """
        Generate the FactSales table.
        """

        records = []

        customers = self.customers["CustomerID"].tolist()

        stores = self.stores["StoreID"].tolist()

        dates = self.dates["DateKey"].tolist()

        products = (
            self.products
            .set_index("ProductID")
            .to_dict("index")
        )

        product_ids = list(products.keys())

        employees = self.employees[
            self.employees["JobTitle"].isin(
                ELIGIBLE_JOB_TITLES
            )
        ]

        employee_ids = employees["EmployeeID"].tolist()
        for sale_number in range(1, NUM_SALES + 1):

            sales_id = f"SAL{sale_number:08d}"

            receipt_number = (
                f"RCP{sale_number:010d}"
            )

            customer_id = random.choice(customers)

            product_id = random.choice(product_ids)

            store_id = random.choice(stores)

            employee_id = random.choice(employee_ids)

            date_key = random.choice(dates)

            product = products[product_id]

            selling_price = float(
                product["SellingPrice"]
            )

            unit_cost = float(
                product["UnitCost"]
            )

            vat_rate = float(
                product["VATRate"]
            )

            quantity = random.choices(
                population=[
                    1, 2, 3, 4, 5,
                    10, 15, 20,
                ],
                weights=[
                    30, 25, 18, 10,
                    8, 5, 3, 1,
                ],
                k=1,
            )[0]

            discount_pct = random.choices(
                population=[
                    0,
                    5,
                    10,
                    15,
                    20,
                ],
                weights=[
                    65,
                    15,
                    10,
                    7,
                    3,
                ],
                k=1,
            )[0]

            amounts = self._amounts(
                quantity=quantity,
                selling_price=selling_price,
                unit_cost=unit_cost,
                discount_pct=discount_pct,
                vat_rate=vat_rate,
            )

            payment_method = random.choices(
                population=PAYMENT_METHODS,
                weights=[50, 30, 15, 5],
                k=1,
            )[0]

            sales_channel = random.choices(
                population=SALES_CHANNELS,
                weights=[90, 8, 2],
                k=1,
            )[0]

            sales_status = random.choices(
                population=SALES_STATUS,
                weights=[97, 2, 1],
                k=1,
            )[0]

            hour = random.choices(
                population=[
                    8, 9, 10, 11,
                    12, 13, 14, 15,
                    16, 17, 18, 19, 20,
                ],
                weights=[
                    3, 4, 5, 6,
                    8, 9, 10, 10,
                    10, 11, 12, 8, 4,
                ],
                k=1,
            )[0]

            minute = random.randint(0, 59)

            second = random.randint(0, 59)

            transaction_time = (
                f"{hour:02d}:"
                f"{minute:02d}:"
                f"{second:02d}"
            )

            records.append(
                {
                    "SalesID": sales_id,
                    "SalesNumber": receipt_number,
                    "ReceiptNumber": receipt_number,
                    "DateKey": date_key,
                    "CustomerID": customer_id,
                    "StoreID": store_id,
                    "EmployeeID": employee_id,
                    "ProductID": product_id,
                    "QuantitySold": quantity,
                    "UnitPrice": selling_price,
                    "GrossAmount": amounts.gross,
                    "DiscountPct": discount_pct,
                    "DiscountAmount": amounts.discount,
                    "NetAmount": amounts.net,
                    "VATRate": vat_rate,
                    "VATAmount": amounts.vat,
                    "TotalAmount": amounts.total,
                    "CostAmount": amounts.cost,
                    "ProfitAmount": amounts.profit,
                    "ProfitMarginPct": amounts.margin,
                    "PaymentMethod": payment_method,
                    "SalesChannel": sales_channel,
                    "TransactionTime": transaction_time,
                    "SalesStatus": sales_status,
                }
            )

            if sale_number % 25000 == 0:

                logger.info(
                    f"Sales generation progress: "
                    f"{sale_number:,} / {NUM_SALES:,}"
                )

        df = pd.DataFrame(records)

        return df
    def validate(
        self,
        df: pd.DataFrame,
    ) -> None:
        """
        Validate the generated FactSales table.
        """

        validate_dataframe(

            df=df,

            id_column="SalesID",

            unique_columns=[
                "SalesID",
                "ReceiptNumber",
            ],

            required_columns=[
                "SalesID",
                "ReceiptNumber",
                "DateKey",
                "CustomerID",
                "StoreID",
                "EmployeeID",
                "ProductID",
                "QuantitySold",
                "UnitPrice",
                "GrossAmount",
                "NetAmount",
                "VATRate",
                "VATAmount",
                "TotalAmount",
                "PaymentMethod",
                "SalesStatus",
            ],

            numeric_columns=[
                "QuantitySold",
                "UnitPrice",
                "GrossAmount",
                "DiscountPct",
                "DiscountAmount",
                "NetAmount",
                "VATRate",
                "VATAmount",
                "TotalAmount",
                "CostAmount",
            
            ],
        )
        
        employee_title = (
            self.employees
            .set_index("EmployeeID")["JobTitle"]
        )

        if (
            ~df["EmployeeID"]
            .map(employee_title)
            .isin(ELIGIBLE_JOB_TITLES)
        ).any():

            raise ValueError(
                "Unauthorized employee found in FactSales."
            )

                # -----------------------------------------------------
        # Profit Analysis
        # -----------------------------------------------------

        negative_profit = (
            df["ProfitAmount"] < 0
        ).sum()

        logger.info(
            f"Negative Profit Transactions : {negative_profit:,}"
        )
        financial_columns = {

            "GrossAmount": "gross",

            "DiscountAmount": "discount",

            "NetAmount": "net",

            "VATAmount": "vat",

            "TotalAmount": "total",

            "CostAmount": "cost",


        }

        for _, row in df.iterrows():

            expected = self._amounts(

                quantity=int(row["QuantitySold"]),

                selling_price=float(row["UnitPrice"]),

                unit_cost=float(row["CostAmount"])
                / int(row["QuantitySold"]),

                discount_pct=float(row["DiscountPct"]),

                vat_rate=float(row["VATRate"]),

            )

            for column, attribute in financial_columns.items():

                actual = round(
                    float(row[column]),
                    2,
                )

                expected_value = round(
                    getattr(expected, attribute),
                    2,
                )

                if actual != expected_value:

                    raise ValueError(

                        f"\nSalesID: {row['SalesID']}\n"

                        f"Column: {column}\n"

                        f"Expected: {expected_value}\n"

                        f"Actual: {actual}"

                    )
    @timer
    def run(self) -> pd.DataFrame:

        df = self.generate()

        self.validate(df)

        export_dataframe(
            df=df,
            filepath=GENERATED_DATA / "FactSales.csv",
        )

        generation_summary(
            df=df,
            table_name="FactSales",
        )

        return df


def main() -> None:

    SalesGenerator().run()


if __name__ == "__main__":

    main()