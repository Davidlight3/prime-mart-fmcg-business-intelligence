"""PrimeMart FMCG Analytics Platform - Purchase Fact Generator."""
from __future__ import annotations

import logging
import random
from dataclasses import dataclass
from typing import Any

from numpy import diff
import pandas as pd

from config import GENERATED_DATA, NUM_PURCHASES, RANDOM_SEED
from utils import export_dataframe, generation_summary, load_dimension, timer, validate_dataframe

logger = logging.getLogger(__name__)

STORE_PURCHASE_RULES = {
    "Express": (30, 150), "Supermarket": (150, 500),
    "Hypermarket": (500, 1200), "Warehouse": (1200, 5000),
}
DISCOUNT_RULES = ((200, 0.0), (500, 2.0), (1000, 5.0), (float("inf"), 8.0))
PURCHASE_STATUS_WEIGHTS = {"Received": 92, "Pending": 6, "Cancelled": 2}
ELIGIBLE_JOB_TITLES = frozenset({"Procurement Officer", "Assistant Manager", "Store Manager"})
PROGRESS_INTERVAL = 25_000


@dataclass(frozen=True)
class PurchaseAmounts:
    gross: float
    discount: float
    net: float
    vat: float
    total: float


class PurchaseGenerator:
    """Generate, validate, and export FactPurchases."""

    def __init__(self, num_purchases: int = NUM_PURCHASES, seed: int = RANDOM_SEED) -> None:
        if num_purchases <= 0:
            raise ValueError("num_purchases must be greater than zero.")
        self.num_purchases = num_purchases
        self.rng = random.Random(seed)
        self._load_dimensions()
        self._validate_sources()
        self._build_lookups()

    def _load_dimensions(self) -> None:
        self.products = load_dimension("DimProduct")
        self.suppliers = load_dimension("DimSupplier")
        self.stores = load_dimension("DimStore")
        self.employees = load_dimension("DimEmployee")
        self.dates = load_dimension("DimDate")
        self.procurement_employees = self.employees[
            self.employees["JobTitle"].isin(ELIGIBLE_JOB_TITLES)
        ].copy()

    @staticmethod
    def _require(df: pd.DataFrame, name: str, cols: set[str]) -> None:
        missing = cols - set(df.columns)
        if missing:
            raise ValueError(f"{name} missing columns: {sorted(missing)}")

    def _validate_sources(self) -> None:
        self._require(self.products, "DimProduct", {"ProductID", "Category", "UnitCost", "VATRate"})
        self._require(self.suppliers, "DimSupplier", {"SupplierID", "CategorySupplied", "PaymentTerms", "State"})
        self._require(self.stores, "DimStore", {"StoreID", "StoreType"})
        self._require(self.employees, "DimEmployee", {"EmployeeID", "StoreID", "JobTitle"})
        self._require(self.dates, "DimDate", {"DateKey", "IsWeekend"})
        if any(x.empty for x in (self.products, self.suppliers, self.stores, self.dates)):
            raise ValueError("One or more required dimensions are empty.")
        if self.procurement_employees.empty:
            raise ValueError("No eligible procurement/management employees found.")
        bad_types = set(self.stores["StoreType"].dropna()) - set(STORE_PURCHASE_RULES)
        if bad_types:
            raise ValueError(f"Unsupported StoreType values: {sorted(bad_types)}")
        bad_categories = set(self.suppliers["CategorySupplied"].dropna().astype(str)) - set(self.products["Category"].dropna().astype(str))
        if bad_categories:
            raise ValueError(f"Supplier categories without products: {sorted(bad_categories)}")

    @staticmethod
    def _boolish(value: Any) -> bool:
        if isinstance(value, bool):
            return value
        s = str(value).strip().lower()
        if s in {"true", "1", "yes", "y"}: return True
        if s in {"false", "0", "no", "n"}: return False
        raise ValueError(f"Invalid IsWeekend value: {value!r}")

    def _build_lookups(self) -> None:
        self.supplier_records = self.suppliers.to_dict("records")
        self.products_by_category = {
            str(k): g.to_dict("records") for k, g in self.products.groupby("Category", sort=False)
        }
        self.employees_by_store = {
            str(k): g.to_dict("records") for k, g in self.procurement_employees.groupby("StoreID", sort=False)
        }
        self.store_records = [
            r for r in self.stores.to_dict("records") if str(r["StoreID"]) in self.employees_by_store
        ]
        if not self.store_records:
            raise ValueError("No stores have eligible purchasing employees.")
        self.weekday_date_keys, self.weekend_date_keys = [], []
        for row in self.dates[["DateKey", "IsWeekend"]].itertuples(index=False):
            (self.weekend_date_keys if self._boolish(row.IsWeekend) else self.weekday_date_keys).append(int(row.DateKey))
        if not self.weekday_date_keys or not self.weekend_date_keys:
            raise ValueError("DimDate must contain both weekday and weekend dates.")

    def _date_key(self) -> int:
        weekend = self.rng.choices([False, True], weights=[90, 10], k=1)[0]
        return self.rng.choice(self.weekend_date_keys if weekend else self.weekday_date_keys)

    def _quantity(self, store_type: str) -> int:
        lo, hi = STORE_PURCHASE_RULES[store_type]
        return self.rng.randint(lo, hi)

    @staticmethod
    def _discount_pct(quantity: int) -> float:
        return next(pct for upper, pct in DISCOUNT_RULES if quantity < upper)

    def _lead_time(self, state: str) -> int:
        return self.rng.randint(1, 3) if state.strip().casefold() == "lagos" else self.rng.randint(4, 10)

    def _status(self) -> str:
        return self.rng.choices(list(PURCHASE_STATUS_WEIGHTS), weights=list(PURCHASE_STATUS_WEIGHTS.values()), k=1)[0]

    @staticmethod
    def _amounts(quantity: int, unit_cost: float, discount_pct: float, vat_rate: float) -> PurchaseAmounts:
        if quantity <= 0 or unit_cost < 0 or not 0 <= discount_pct <= 100 or vat_rate < 0:
            raise ValueError("Invalid financial inputs.")
        gross = round(quantity * unit_cost, 2)
        discount = round(gross * discount_pct / 100, 2)
        net = round(gross - discount, 2)
        vat = round(net * vat_rate / 100, 2)
        return PurchaseAmounts(gross, discount, net, vat, round(net + vat, 2))

    def _record(self, i: int) -> dict[str, Any]:
        date_key = self._date_key()
        supplier = self.rng.choice(self.supplier_records)
        category = str(supplier["CategorySupplied"])
        product = self.rng.choice(self.products_by_category[category])
        store = self.rng.choice(self.store_records)
        employee = self.rng.choice(self.employees_by_store[str(store["StoreID"])])
        quantity = self._quantity(str(store["StoreType"]))
        discount_pct = self._discount_pct(quantity)
        amounts = self._amounts(quantity, float(product["UnitCost"]), discount_pct, float(product["VATRate"]))
        ds = str(date_key)
        return {
            "PurchaseID": f"PUR{i:08d}", "PurchaseNumber": f"PO-{ds[:4]}-{ds[4:6]}-{i:08d}",
            "DateKey": date_key, "SupplierID": supplier["SupplierID"], "ProductID": product["ProductID"],
            "StoreID": store["StoreID"], "EmployeeID": employee["EmployeeID"], "QuantityPurchased": quantity,
            "UnitCost": float(product["UnitCost"]), "GrossAmount": amounts.gross, "DiscountPct": discount_pct,
            "DiscountAmount": amounts.discount, "NetAmount": amounts.net, "VATRate": float(product["VATRate"]),
            "VATAmount": amounts.vat, "TotalAmount": amounts.total, "PaymentTerms": supplier["PaymentTerms"],
            "LeadTimeDays": self._lead_time(str(supplier["State"])), "PurchaseStatus": self._status(),
        }

    def generate(self) -> pd.DataFrame:
        records = []
        for i in range(1, self.num_purchases + 1):
            records.append(self._record(i))
            if i % PROGRESS_INTERVAL == 0 or i == self.num_purchases:
                logger.info("Purchase generation progress: %s / %s", f"{i:,}", f"{self.num_purchases:,}")
        df = pd.DataFrame.from_records(records)
        if len(df) != self.num_purchases:
            raise RuntimeError("Generated row count does not match NUM_PURCHASES.")
        return df

    def validate(self, df: pd.DataFrame) -> None:
        validate_dataframe(
            df=df, id_column="PurchaseID", unique_columns=["PurchaseID", "PurchaseNumber"],
            required_columns=["PurchaseID", "PurchaseNumber", "DateKey", "SupplierID", "ProductID", "StoreID",
                              "EmployeeID", "QuantityPurchased", "UnitCost", "GrossAmount", "NetAmount",
                              "VATRate", "VATAmount", "TotalAmount", "PaymentTerms", "PurchaseStatus"],
            numeric_columns=["QuantityPurchased", "UnitCost", "GrossAmount", "DiscountPct", "DiscountAmount",
                             "NetAmount", "VATRate", "VATAmount", "TotalAmount", "LeadTimeDays"],
        )
        valid = {
            "DateKey": set(self.dates["DateKey"]), "SupplierID": set(self.suppliers["SupplierID"]),
            "ProductID": set(self.products["ProductID"]), "StoreID": set(self.stores["StoreID"]),
            "EmployeeID": set(self.employees["EmployeeID"]),
        }
        for col, values in valid.items():
            n = int((~df[col].isin(values)).sum())
            if n:
                raise ValueError(f"{n:,} invalid {col} foreign keys.")

        supplier_cat = self.suppliers.set_index("SupplierID")["CategorySupplied"]
        product_cat = self.products.set_index("ProductID")["Category"]
        if (df["SupplierID"].map(supplier_cat) != df["ProductID"].map(product_cat)).any():
            raise ValueError("Supplier/product category business rule failed.")

        employee_store = self.employees.set_index("EmployeeID")["StoreID"]
        if (df["EmployeeID"].map(employee_store).astype(str) != df["StoreID"].astype(str)).any():
            raise ValueError("Employee/store business rule failed.")

                # -----------------------------------------------------
        # Validate Authorized Employees
        # -----------------------------------------------------

        employee_title = (
            self.employees
            .set_index("EmployeeID")["JobTitle"]
        )

        unauthorized = (
            ~df["EmployeeID"]
            .map(employee_title)
            .isin(ELIGIBLE_JOB_TITLES)
        )

        if unauthorized.any():
            raise ValueError(
                "Unauthorized employee found in FactPurchases."
            )
        # -----------------------------------------------------
        # Financial Reconciliation
        # -----------------------------------------------------

        financial_columns = [
            "GrossAmount",
            "DiscountAmount",
            "NetAmount",
            "VATAmount",
            "TotalAmount",
        ]

        for _, row in df.iterrows():

            expected = self._amounts(
                quantity=int(row["QuantityPurchased"]),
                unit_cost=float(row["UnitCost"]),
                discount_pct=float(row["DiscountPct"]),
                vat_rate=float(row["VATRate"]),
            )

            expected_values = {
                "GrossAmount": expected.gross,
                "DiscountAmount": expected.discount,
                "NetAmount": expected.net,
                "VATAmount": expected.vat,
                "TotalAmount": expected.total,
            }

            for column in financial_columns:

                actual = round(float(row[column]), 2)
                expected_value = round(expected_values[column], 2)

                if actual != expected_value:

                    raise ValueError(
                        f"\nPurchaseID: {row['PurchaseID']}\n"
                        f"Column: {column}\n"
                        f"Expected: {expected_value}\n"
                        f"Actual: {actual}"
                    )

        

    @timer
    def run(self) -> pd.DataFrame:
        df = self.generate()
        self.validate(df)
        export_dataframe(df=df, filepath=GENERATED_DATA / "FactPurchases.csv")
        generation_summary(df=df, table_name="FactPurchases")
        return df


def main() -> None:
    PurchaseGenerator().run()


if __name__ == "__main__":
    main()
