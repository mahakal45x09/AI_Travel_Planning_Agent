"""
Clean TripAdvisor Reviews Dataset
=================================
Cleans user preference ratings and maps generic category names to meaningful ones.
"""

import pandas as pd
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEANED_DIR = os.path.join(BASE_DIR, "cleaned")
os.makedirs(CLEANED_DIR, exist_ok=True)

# Map generic category numbers to meaningful TripAdvisor category names
# Based on common TripAdvisor review categories
CATEGORY_MAPPING = {
    "Category 1": "art_galleries",
    "Category 2": "dance_clubs",
    "Category 3": "juice_bars",
    "Category 4": "restaurants",
    "Category 5": "museums",
    "Category 6": "resorts",
    "Category 7": "parks_picnic_spots",
    "Category 8": "beaches",
    "Category 9": "theaters",
    "Category 10": "religious_sites",
}


def clean_reviews(input_path: str, output_path: str):
    """Clean TripAdvisor user preference ratings."""
    print("Loading TripAdvisor review data...")
    df = pd.read_csv(input_path)
    print(f"  Raw records: {len(df)}")

    # --- Step 1: Rename categories ---
    df = df.rename(columns=CATEGORY_MAPPING)
    print(f"  Renamed {len(CATEGORY_MAPPING)} categories to meaningful names")

    # --- Step 2: Normalize ratings to 0-5 scale ---
    rating_cols = list(CATEGORY_MAPPING.values())
    for col in rating_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").clip(0, 5)

    # --- Step 3: Remove users with all-zero ratings ---
    row_sums = df[rating_cols].sum(axis=1)
    df = df[row_sums > 0]
    print(f"  After removing zero-rating users: {len(df)}")

    # --- Step 4: Add preference profile ---
    # Find each user's top preference category
    df["top_preference"] = df[rating_cols].idxmax(axis=1)
    df["avg_rating"] = df[rating_cols].mean(axis=1).round(2)

    # --- Step 5: Clean user IDs ---
    df["User ID"] = df["User ID"].str.strip()

    # --- Stats ---
    print(f"\n  Preference distribution:")
    print(df["top_preference"].value_counts().head(5).to_string())
    print(f"\n  Avg rating across all users: {df['avg_rating'].mean():.2f}")

    # --- Save ---
    df.to_csv(output_path, index=False)
    print(f"\n✅ Saved to: {output_path}")

    return df


if __name__ == "__main__":
    input_path = os.path.join(BASE_DIR, "tripadvisor_review.csv")
    output_path = os.path.join(CLEANED_DIR, "user_preferences_cleaned.csv")

    if not os.path.exists(input_path):
        print(f"❌ File not found: {input_path}")
        sys.exit(1)

    clean_reviews(input_path, output_path)
