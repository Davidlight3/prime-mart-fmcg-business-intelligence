import random
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker

from config import GENERATED_DATA, NUM_CUSTOMERS
from constants import (
    CUSTOMER_SEGMENTS,
    PAYMENT_METHODS,
    NIGERIAN_STATES,
)

from utils import (
    generate_id,
    generate_phone,
    generate_email,
    generate_location,
    random_status,
    export_dataframe,
    validate_dataframe,
    generation_summary,
    timer,
)

fake = Faker()


def calculate_age(date_of_birth):
    """Calculate age from date of birth."""
    today = datetime.today().date()

    return (
        today.year
        - date_of_birth.year
        - (
            (today.month, today.day)
            < (date_of_birth.month, date_of_birth.day)
        )
    )


def generate_registration_date(date_of_birth):
    """
    Customer cannot register before turning 18.
    """

    eighteenth_birthday = date_of_birth + timedelta(days=18 * 365)

    start = max(
        eighteenth_birthday,
        datetime(2018, 1, 1).date()
    )

    end = datetime.today().date()

    days = (end - start).days

    return start + timedelta(days=random.randint(0, days))


def customer_profile(segment):
    """
    Returns Loyalty Points and Lifetime Value
    based on customer segment.
    """

    if segment == "Retail":
        loyalty = random.randint(0, 8000)
        lifetime = round(random.uniform(50000, 800000), 2)

    elif segment == "Wholesale":
        loyalty = random.randint(8000, 25000)
        lifetime = round(random.uniform(2000000, 20000000), 2)

    elif segment == "Distributor":
        loyalty = random.randint(12000, 35000)
        lifetime = round(random.uniform(5000000, 50000000), 2)

    else:  # VIP
        loyalty = random.randint(20000, 60000)
        lifetime = round(random.uniform(10000000, 100000000), 2)

    return loyalty, lifetime
@timer
def generate_customers():

    customers = []

    segment_weights = [
    65,   # Retail
    15,   # Wholesale
    15,   # Distributor
    5     # VIP
]

    for i in range(1, NUM_CUSTOMERS + 1):

        customer_id = generate_id("CUS", i)

        customer_code = f"CUST{i:06d}"

        gender = random.choice(
            [
                "Male",
                "Female",
            ]
        )

        if gender == "Male":
            first_name = fake.first_name_male()
        else:
            first_name = fake.first_name_female()

        last_name = fake.last_name()

        dob = fake.date_of_birth(
            minimum_age=18,
            maximum_age=80,
        )

        age = calculate_age(dob)

        email = generate_email(
            first_name,
            last_name,
        )

        phone = generate_phone()

        state, city = generate_location(
            NIGERIAN_STATES
        )

        segment = random.choices(
            CUSTOMER_SEGMENTS,
            weights=segment_weights,
            k=1,
        )[0]

        loyalty_points, lifetime_value = customer_profile(
            segment
        )

        registration_date = generate_registration_date(
            dob
        )

        payment_method = random.choice(
            PAYMENT_METHODS
        )

        status = random_status(93)

        customers.append(
            {
                "CustomerID": customer_id,
                "CustomerCode": customer_code,
                "FirstName": first_name,
                "LastName": last_name,
                "Gender": gender,
                "DateOfBirth": dob,
                "Age": age,
                "Email": email,
                "Phone": phone,
                "State": state,
                "City": city,
                "CustomerSegment": segment,
                "RegistrationDate": registration_date,
                "LoyaltyPoints": loyalty_points,
                "PreferredPaymentMethod": payment_method,
                "LifetimeValue": lifetime_value,
                "Status": status,
            }
        )

            # =====================================================
    # CREATE DATAFRAME
    # =====================================================

    df = pd.DataFrame(customers)

    # =====================================================
    # VALIDATE DATA
    # =====================================================

    validate_dataframe(
        df=df,
        id_column="CustomerID",
        unique_columns=[
            "CustomerID",
            "CustomerCode",
        ],
        required_columns=[
            "FirstName",
            "LastName",
            "Gender",
            "Email",
            "Phone",
            "State",
            "City",
            "CustomerSegment",
        ],
    )

# =====================================================
# EXPORT
# =====================================================

    export_dataframe(
    df,
    GENERATED_DATA / "DimCustomer.csv"
)

    # =====================================================
    # SUMMARY
    # =====================================================

    generation_summary(
        df=df,
        table_name="DimCustomer",
    )

    return df


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":
    generate_customers()