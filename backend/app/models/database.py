"""
Database Service
================
Loads cleaned CSV data into SQLite and provides query functions.
Also manages ChromaDB vector store for semantic search.
"""

import pandas as pd
import sqlite3
import os
import json
from pathlib import Path
from typing import Optional

from app.config import CLEANED_DATA_DIR, settings

# Database path
DB_PATH = Path(settings.database_url.replace("sqlite:///", ""))


class TravelDatabase:
    """Manages SQLite database with travel data."""

    def __init__(self, db_path: str = None):
        self.db_path = db_path or str(DB_PATH)
        self.conn = None

    def connect(self):
        """Connect to SQLite database."""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        return self.conn

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()

    def init_db(self):
        """Initialize database with cleaned data from CSV files."""
        print("🔄 Initializing database...")
        self.connect()

        # Load each cleaned CSV into a SQLite table
        data_files = {
            "destinations_india": "destinations_india.csv",
            "destinations_world": "destinations_world.csv",
            "airports": "airports_cleaned.csv",
            "countries": "countries_cleaned.csv",
            "travel_details": "travel_details_cleaned.csv",
            "user_preferences": "user_preferences_cleaned.csv",
        }

        for table_name, csv_file in data_files.items():
            csv_path = CLEANED_DATA_DIR / csv_file
            if csv_path.exists():
                df = pd.read_csv(csv_path)
                df.to_sql(table_name, self.conn, if_exists="replace", index=False)
                print(f"  ✅ Loaded {table_name}: {len(df)} rows")
            else:
                print(f"  ⚠️  Skipped {table_name}: {csv_file} not found")

        # Create indexes for faster queries
        self._create_indexes()
        print("✅ Database initialized!")

    def _create_indexes(self):
        """Create indexes for common queries."""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_india_state ON destinations_india(state)",
            "CREATE INDEX IF NOT EXISTS idx_india_category ON destinations_india(category)",
            "CREATE INDEX IF NOT EXISTS idx_india_place ON destinations_india(place_name)",
            "CREATE INDEX IF NOT EXISTS idx_world_country ON destinations_world(country)",
            "CREATE INDEX IF NOT EXISTS idx_world_continent ON destinations_world(continent)",
            "CREATE INDEX IF NOT EXISTS idx_world_category ON destinations_world(category)",
            "CREATE INDEX IF NOT EXISTS idx_airports_country ON airports(country_code)",
            "CREATE INDEX IF NOT EXISTS idx_airports_iata ON airports(iata_code)",
            "CREATE INDEX IF NOT EXISTS idx_airports_city ON airports(city)",
            "CREATE INDEX IF NOT EXISTS idx_countries_name ON countries(name)",
        ]
        cursor = self.conn.cursor()
        for sql in indexes:
            cursor.execute(sql)
        self.conn.commit()

    # === Query Methods ===

    def search_india_destinations(
        self,
        query: str = None,
        state: str = None,
        category: str = None,
        max_budget: int = None,
        limit: int = 10,
    ) -> list[dict]:
        """Search Indian destinations with filters."""
        sql = "SELECT * FROM destinations_india WHERE 1=1"
        params = []

        if query:
            sql += " AND (place_name LIKE ? OR description LIKE ? OR state LIKE ?)"
            q = f"%{query}%"
            params.extend([q, q, q])

        if state:
            sql += " AND state LIKE ?"
            params.append(f"%{state}%")

        if category:
            sql += " AND category LIKE ?"
            params.append(f"%{category}%")

        if max_budget:
            sql += " AND avg_budget_per_day_inr <= ?"
            params.append(max_budget)

        sql += " ORDER BY rating DESC LIMIT ?"
        params.append(limit)

        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        return [dict(row) for row in cursor.fetchall()]

    def search_world_destinations(
        self,
        query: str = None,
        country: str = None,
        continent: str = None,
        category: str = None,
        max_budget: int = None,
        limit: int = 10,
    ) -> list[dict]:
        """Search world destinations with filters."""
        sql = "SELECT * FROM destinations_world WHERE 1=1"
        params = []

        if query:
            sql += " AND (place_name LIKE ? OR description LIKE ? OR country LIKE ?)"
            q = f"%{query}%"
            params.extend([q, q, q])

        if country:
            sql += " AND country LIKE ?"
            params.append(f"%{country}%")

        if continent:
            sql += " AND continent LIKE ?"
            params.append(f"%{continent}%")

        if category:
            sql += " AND category LIKE ?"
            params.append(f"%{category}%")

        if max_budget:
            sql += " AND avg_budget_per_day_usd <= ?"
            params.append(max_budget)

        sql += " ORDER BY rating DESC LIMIT ?"
        params.append(limit)

        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        return [dict(row) for row in cursor.fetchall()]

    def get_destination_details(self, place_name: str) -> Optional[dict]:
        """Get full details for a specific destination."""
        cursor = self.conn.cursor()

        # Check India first
        cursor.execute(
            "SELECT * FROM destinations_india WHERE place_name LIKE ?",
            [f"%{place_name}%"],
        )
        row = cursor.fetchone()
        if row:
            result = dict(row)
            result["source"] = "india"
            return result

        # Check world
        cursor.execute(
            "SELECT * FROM destinations_world WHERE place_name LIKE ?",
            [f"%{place_name}%"],
        )
        row = cursor.fetchone()
        if row:
            result = dict(row)
            result["source"] = "world"
            return result

        return None

    def find_airports(self, city: str = None, country_code: str = None, limit: int = 5) -> list[dict]:
        """Find airports by city or country."""
        sql = "SELECT * FROM airports WHERE 1=1"
        params = []

        if city:
            sql += " AND (city LIKE ? OR airport_name LIKE ?)"
            q = f"%{city}%"
            params.extend([q, q])

        if country_code:
            sql += " AND country_code = ?"
            params.append(country_code)

        sql += " ORDER BY airport_type ASC LIMIT ?"
        params.append(limit)

        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        return [dict(row) for row in cursor.fetchall()]

    def get_country_info(self, country_name: str) -> Optional[dict]:
        """Get country metadata."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM countries WHERE name LIKE ? OR country_code_2 = ?",
            [f"%{country_name}%", country_name.upper()],
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_all_india_states(self) -> list[str]:
        """Get list of all Indian states with destinations."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT state FROM destinations_india ORDER BY state")
        return [row["state"] for row in cursor.fetchall()]

    def get_all_categories(self, source: str = "india") -> list[str]:
        """Get list of all categories."""
        table = "destinations_india" if source == "india" else "destinations_world"
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT DISTINCT category FROM {table} ORDER BY category")
        return [row["category"] for row in cursor.fetchall()]

    def get_stats(self) -> dict:
        """Get database statistics."""
        cursor = self.conn.cursor()
        stats = {}

        for table in ["destinations_india", "destinations_world", "airports", "countries"]:
            try:
                cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                stats[table] = cursor.fetchone()["count"]
            except Exception:
                stats[table] = 0

        return stats


# Global database instance
db = TravelDatabase()
