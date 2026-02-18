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

        CREATE TABLE IF NOT EXISTS learning_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id INTEGER REFERENCES profiles(id),
            topic TEXT NOT NULL,
            level TEXT CHECK(level IN ('입문', '중급', '고급')),
            status TEXT CHECK(status IN ('추천', '학습중', '완료')),
            expert_source TEXT,
            started_at TIMESTAMP,
            completed_at TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS session_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id INTEGER REFERENCES profiles(id),
            session_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_level TEXT,
            selected_strategy TEXT,
            matched_experts TEXT,
            selected_workflows TEXT,
            roadmap_path TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_profiles_updated ON profiles(updated_at DESC);
        CREATE INDEX IF NOT EXISTS idx_agent_results_profile ON agent_results(profile_id);
        CREATE INDEX IF NOT EXISTS idx_learning_progress_profile ON learning_progress(profile_id);
        CREATE INDEX IF NOT EXISTS idx_session_history_profile ON session_history(profile_id, session_date DESC);
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
