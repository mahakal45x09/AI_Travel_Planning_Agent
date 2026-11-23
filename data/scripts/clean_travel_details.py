"""
Clean Travel Details Dataset
=============================
Cleans the small (139 rows) travel details dataset.
- Standardizes dates to ISO format
- Splits destination into city + country
- Normalizes cost columns
- Adds currency column
"""

import pandas as pd
import os
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEANED_DIR = os.path.join(BASE_DIR, "cleaned")
os.makedirs(CLEANED_DIR, exist_ok=True)


def parse_date(date_str: str) -> str:
    """Convert various date formats to ISO YYYY-MM-DD."""
    if pd.isna(date_str) or str(date_str).strip() == "":
        return ""
    date_str = str(date_str).strip()
    formats = [
        "%m/%d/%Y", "%d/%m/%Y", "%Y-%m-%d",
        "%m-%d-%Y", "%d-%m-%Y", "%B %d, %Y"
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return date_str  # Return as-is if unparseable


def split_destination(dest: str) -> tuple:
    """Split 'London, UK' into ('London', 'United Kingdom')."""
    country_map = {
        "UK": "United Kingdom",
        "USA": "United States",
        "UAE": "United Arab Emirates",
    }
    if pd.isna(dest):
        return ("", "")
    parts = [p.strip() for p in str(dest).split(",")]
    city = parts[0] if len(parts) > 0 else ""
    country = parts[1] if len(parts) > 1 else ""
    country = country_map.get(country, country)
    return (city, country)


def clean_travel_details(input_path: str, output_path: str):
    """Clean travel details dataset."""
    print("Loading travel details data...")
    df = pd.read_csv(input_path)
    print(f"  Raw records: {len(df)}")

    # --- Step 1: Split destination ---
    dest_split = df["Destination"].apply(split_destination)
    df["city"] = dest_split.apply(lambda x: x[0])
    df["country"] = dest_split.apply(lambda x: x[1])

    # --- Step 2: Standardize dates ---
    df["start_date"] = df["Start date"].apply(parse_date)
    df["end_date"] = df["End date"].apply(parse_date)

    # --- Step 3: Clean numeric columns ---
    for col in ["Duration (days)", "Accommodation cost", "Transportation cost", "Traveler age"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # --- Step 4: Calculate total cost ---
    df["total_cost_usd"] = (
        df["Accommodation cost"].fillna(0) + df["Transportation cost"].fillna(0)
    )

    # --- Step 5: Add currency ---
    df["currency"] = "USD"

    # --- Step 6: Rename and select columns ---
    df_clean = df[[
        "Trip ID", "city", "country", "start_date", "end_date",
        "Duration (days)", "Traveler name", "Traveler age",
        "Traveler gender", "Traveler nationality",
        "Accommodation type", "Accommodation cost",
        "Transportation type", "Transportation cost",
        "total_cost_usd", "currency"
    ]].copy()

    df_clean.columns = [
        "trip_id", "city", "country", "start_date", "end_date",
        "duration_days", "traveler_name", "traveler_age",
        "traveler_gender", "traveler_nationality",
        "accommodation_type", "accommodation_cost_usd",
        "transport_type", "transport_cost_usd",
        "total_cost_usd", "currency"
    ]

    # --- Step 7: Remove nulls ---
    df_clean = df_clean.dropna(subset=["city", "country"])
    print(f"  After cleaning: {len(df_clean)}")

    # --- Stats ---
    india_trips = df_clean[df_clean["country"].str.contains("India", case=False, na=False)]
    print(f"  India trips: {len(india_trips)}")
    print(f"  Unique destinations: {df_clean['city'].nunique()}")
    print(f"  Avg total cost: ${df_clean['total_cost_usd'].mean():.0f}")

    # --- Save ---
    df_clean.to_csv(output_path, index=False)
    print(f"\n✅ Saved to: {output_path}")

    return df_clean


if __name__ == "__main__":
    input_path = os.path.join(BASE_DIR, "Travel details dataset.csv")
    output_path = os.path.join(CLEANED_DIR, "travel_details_cleaned.csv")

    if not os.path.exists(input_path):
        print(f"❌ File not found: {input_path}")
        sys.exit(1)

    clean_travel_details(input_path, output_path)
