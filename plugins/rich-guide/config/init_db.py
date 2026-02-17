#!/usr/bin/env python3
"""Initialize Rich Guide SQLite database. Usage: python3 init_db.py <db_path>"""

import sqlite3
import sys
import os


def init_db(db_path: str) -> None:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            monthly_income INTEGER,
            monthly_expense INTEGER,
            savings INTEGER,
            investment_assets INTEGER,
            debt INTEGER,
            risk_tolerance TEXT CHECK(risk_tolerance IN ('low', 'medium', 'high')),
            goal TEXT
        );

        CREATE TABLE IF NOT EXISTS agent_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id INTEGER REFERENCES profiles(id),
            agent_name TEXT NOT NULL,
            execution_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            result_json TEXT,
            status TEXT CHECK(status IN ('success', 'failed', 'partial'))
        );

        CREATE INDEX IF NOT EXISTS idx_profiles_updated ON profiles(updated_at DESC);
        CREATE INDEX IF NOT EXISTS idx_agent_results_profile ON agent_results(profile_id);
    """)

    conn.commit()
    conn.close()
    print(f"DB initialized: {db_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        default_path = os.path.expanduser("~/.claude/skills/rich-guide/data/profiles.db")
        init_db(default_path)
    else:
        init_db(sys.argv[1])
