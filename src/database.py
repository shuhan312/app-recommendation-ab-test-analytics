"""
database.py
-----------
Creates the SQLite database and loads the cleaned dataset into it.

Usage:
    python src/database.py
"""

import sqlite3
import pandas as pd
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
ROOT        = Path(__file__).resolve().parent.parent
DATA_CLEAN  = ROOT / "data" / "processed" / "cookie_cats_cleaned.csv"
SQL_CREATE  = ROOT / "sql" / "create_tables.sql"
DB_PATH     = ROOT / "data" / "app_ab_test.db"


def create_database():
    """Create SQLite database and load cleaned data."""

    # 1. Load cleaned CSV
    print(f"Loading data from: {DATA_CLEAN}")
    df = pd.read_csv(DATA_CLEAN)
    print(f"  Rows loaded: {len(df):,}")

    # 2. Read the CREATE TABLE SQL
    print(f"Reading schema from: {SQL_CREATE}")
    create_sql = SQL_CREATE.read_text()

    # 3. Connect to SQLite (creates file if it doesn't exist)
    print(f"Connecting to database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 4. Create tables
    cursor.executescript(create_sql)
    conn.commit()
    print("  Table 'users' created ✓")

    # 5. Insert data
    df.to_sql("users", conn, if_exists="append", index=False)
    conn.commit()
    print(f"  Rows inserted: {len(df):,} ✓")

    # 6. Verify
    count = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    sample = cursor.execute(
        "SELECT * FROM users LIMIT 3"
    ).fetchall()

    print(f"\n=== Verification ===")
    print(f"Total rows in DB: {count:,}")
    print(f"Sample rows:")
    for row in sample:
        print(f"  {row}")

    conn.close()
    print(f"\nDatabase saved to: {DB_PATH} ✓")


if __name__ == "__main__":
    create_database()
