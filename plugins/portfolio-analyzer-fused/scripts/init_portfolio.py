#!/usr/bin/env python3
"""
Initialize portfolio database with schema.
Part of portfolio-analyzer-fused plugin.
"""
import sqlite3
import sys
from pathlib import Path

# Database path relative to script location
DB_PATH = Path(__file__).parent.parent / "data" / "portfolio.db"
SCHEMA_PATH = Path(__file__).parent.parent / "config" / "schema.sql"

def init_database():
    """Initialize the database with schema from schema.sql."""
    try:
        # Create data directory if it doesn't exist
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)

        # Check if schema file exists
        if not SCHEMA_PATH.exists():
            print(f"❌ Schema file not found: {SCHEMA_PATH}", file=sys.stderr)
            return 1

        # Connect to database (creates if doesn't exist)
        conn = sqlite3.connect(DB_PATH)

        # Read and execute schema
        with open(SCHEMA_PATH, 'r') as f:
            schema_sql = f.read()
            conn.executescript(schema_sql)

        conn.commit()
        conn.close()

        print(f"✅ Database initialized successfully")
        print(f"📍 Location: {DB_PATH}")
        print(f"📊 Tables created: holdings, transactions, score_history, chat_history, portfolio_meta")

        return 0

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(init_database())
