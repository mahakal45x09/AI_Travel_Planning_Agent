"""
Clean Countries Dataset
=======================
Flattens the nested countries.json into a clean, usable format.
Extracts: name, capital, region, currencies, languages, coordinates, etc.
Exports as both JSON and CSV for flexible use.
"""

import pandas as pd
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEANED_DIR = os.path.join(BASE_DIR, "cleaned")
os.makedirs(CLEANED_DIR, exist_ok=True)


def flatten_country(country: dict) -> dict:
    """Extract key fields from a nested country object."""
    # Name
    name = country.get("name", {}).get("common", "")
    official_name = country.get("name", {}).get("official", "")

    # Capital
    capitals = country.get("capital", [])
    capital = capitals[0] if capitals else ""

    # Region
    region = country.get("region", "")
    subregion = country.get("subregion", "")
    continent = country.get("continents", [""])[0] if country.get("continents") else ""

    # Codes
    cca2 = country.get("cca2", "")
    cca3 = country.get("cca3", "")

    # Currencies
    currencies_raw = country.get("currencies", {})
    currency_codes = list(currencies_raw.keys())
    currency_code = currency_codes[0] if currency_codes else ""
    currency_name = currencies_raw.get(currency_code, {}).get("name", "") if currency_code else ""
    currency_symbol = currencies_raw.get(currency_code, {}).get("symbol", "") if currency_code else ""

    # Languages
    languages_raw = country.get("languages", {})
    languages = ", ".join(languages_raw.values())

    # Coordinates
    latlng = country.get("latlng", [0, 0])
    latitude = latlng[0] if len(latlng) > 0 else 0
    longitude = latlng[1] if len(latlng) > 1 else 0

    # Population
    population = country.get("population", 0)

    # Timezone
    timezones = country.get("timezones", [])
    timezone = timezones[0] if timezones else ""

    # Flag
    flag_emoji = country.get("flag", "")
    flag_png = country.get("flags", {}).get("png", "")

    # Driving side
    car_side = country.get("car", {}).get("side", "")

    # Independent
    independent = country.get("independent", False)
    un_member = country.get("unMember", False)

    return {
        "name": name,
        "official_name": official_name,
        "country_code_2": cca2,
        "country_code_3": cca3,
        "capital": capital,
        "region": region,
        "subregion": subregion,
        "continent": continent,
        "latitude": latitude,
        "longitude": longitude,
        "population": population,
        "currency_code": currency_code,
        "currency_name": currency_name,
        "currency_symbol": currency_symbol,
        "languages": languages,
        "timezone": timezone,
        "flag_emoji": flag_emoji,
        "flag_png": flag_png,
        "driving_side": car_side,
        "independent": independent,
        "un_member": un_member,
    }


def clean_countries(input_path: str, output_csv: str, output_json: str):
    """Clean and flatten countries.json."""
    print("Loading countries data...")
    with open(input_path, "r", encoding="utf-8") as f:
        countries_raw = json.load(f)
    print(f"  Raw countries: {len(countries_raw)}")

    # Flatten each country
    cleaned = [flatten_country(c) for c in countries_raw]

    # Convert to DataFrame
    df = pd.DataFrame(cleaned)

    # Remove entries without names
    df = df[df["name"].str.strip() != ""]
    print(f"  After removing empty names: {len(df)}")

    # Sort by name
    df = df.sort_values("name").reset_index(drop=True)

    # Stats
    print(f"\n  Regions: {df['region'].nunique()}")
    print(f"  Currencies: {df['currency_code'].nunique()}")
    print(f"  Independent nations: {df['independent'].sum()}")
    india = df[df["name"] == "India"]
    if not india.empty:
        print(f"  India found: capital={india.iloc[0]['capital']}, "
              f"currency={india.iloc[0]['currency_code']}")

    # Save CSV
    df.to_csv(output_csv, index=False)
    print(f"\n✅ Saved CSV: {output_csv}")

    # Save JSON
    records = df.to_dict(orient="records")
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved JSON: {output_json}")

    return df


if __name__ == "__main__":
    input_path = os.path.join(BASE_DIR, "countries.json")
    output_csv = os.path.join(CLEANED_DIR, "countries_cleaned.csv")
    output_json = os.path.join(CLEANED_DIR, "countries_cleaned.json")

    if not os.path.exists(input_path):
        print(f"❌ File not found: {input_path}")
        sys.exit(1)

    clean_countries(input_path, output_csv, output_json)
