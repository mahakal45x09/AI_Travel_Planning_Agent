"""
Clean Airports Dataset
======================
Filters the large airports.csv (85K+ rows) down to usable travel airports.
- Keeps only large and medium airports
- Removes entries without IATA codes
- Maps country codes to full names
- Exports cleaned CSV with ~5,000-8,000 airports
"""

import pandas as pd
import json
import os
import sys

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR)
CLEANED_DIR = os.path.join(BASE_DIR, "cleaned")
os.makedirs(CLEANED_DIR, exist_ok=True)


def load_country_mapping(countries_json_path: str) -> dict:
    """Load countries.json and create iso_code -> country_name mapping."""
    with open(countries_json_path, "r", encoding="utf-8") as f:
        countries = json.load(f)

    mapping = {}
    for country in countries:
        cca2 = country.get("cca2", "")
        name = country.get("name", {}).get("common", "")
        if cca2 and name:
            mapping[cca2] = name
    return mapping


def clean_airports(input_path: str, countries_json_path: str, output_path: str):
    """Clean and filter airports dataset."""
    print("Loading airports data...")
    df = pd.read_csv(input_path, low_memory=False)
    print(f"  Raw records: {len(df):,}")

    # --- Step 1: Filter by airport type ---
    valid_types = ["large_airport", "medium_airport"]
    df = df[df["type"].isin(valid_types)]
    print(f"  After type filter (large + medium): {len(df):,}")

    # --- Step 2: Remove rows without IATA codes ---
    df = df.dropna(subset=["iata_code"])
    df = df[df["iata_code"].str.strip() != ""]
    print(f"  After IATA filter: {len(df):,}")

    # --- Step 3: Map country codes to full names ---
    country_map = load_country_mapping(countries_json_path)
    df["country_name"] = df["iso_country"].map(country_map).fillna(df["iso_country"])

    # --- Step 4: Select and rename useful columns ---
    df_clean = df[[
        "iata_code", "name", "municipality", "country_name",
        "iso_country", "iso_region", "continent",
        "latitude_deg", "longitude_deg", "type"
    ]].copy()

    df_clean.columns = [
        "iata_code", "airport_name", "city", "country",
        "country_code", "region_code", "continent",
        "latitude", "longitude", "airport_type"
    ]

    # --- Step 5: Clean string fields ---
    for col in ["iata_code", "airport_name", "city", "country"]:
        df_clean[col] = df_clean[col].str.strip()

    # --- Step 6: Remove duplicates ---
    df_clean = df_clean.drop_duplicates(subset=["iata_code"])
    print(f"  After dedup: {len(df_clean):,}")

    # --- Step 7: Sort by country and city ---
    df_clean = df_clean.sort_values(["country", "city"]).reset_index(drop=True)

    # --- Stats ---
    india_count = len(df_clean[df_clean["country_code"] == "IN"])
    print(f"\n  India airports: {india_count}")
    print(f"  Unique countries: {df_clean['country'].nunique()}")
    print(f"  Total cleaned airports: {len(df_clean):,}")

    # --- Save ---
    df_clean.to_csv(output_path, index=False)
    print(f"\n✅ Saved to: {output_path}")

    return df_clean


if __name__ == "__main__":
    airports_path = os.path.join(RAW_DIR, "airports.csv")
    countries_path = os.path.join(RAW_DIR, "countries.json")
    output_path = os.path.join(CLEANED_DIR, "airports_cleaned.csv")

    if not os.path.exists(airports_path):
        print(f"❌ File not found: {airports_path}")
        sys.exit(1)
    if not os.path.exists(countries_path):
        print(f"❌ File not found: {countries_path}")
        sys.exit(1)

    clean_airports(airports_path, countries_path, output_path)
