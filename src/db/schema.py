"""
SQLite schema definitions for Polymarket Radar.

All CREATE TABLE and schema initialization logic lives here.
"""

import sqlite3
from datetime import datetime, timezone

import config


def init_database(db_path: str = config.DB_PATH) -> sqlite3.Connection:
    """
    Initialize database: create tables if they don't exist.

    Args:
        db_path: Path to SQLite database file.

    Returns:
        Database connection object.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    create_tables(cursor)

    conn.commit()
    return conn


def create_tables(cursor: sqlite3.Cursor) -> None:
    """
    Create all required tables.

    Args:
        cursor: SQLite cursor.
    """
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS markets (
            condition_id TEXT PRIMARY KEY,
            category TEXT,
            question TEXT,
            current_price REAL,
            rolling_volume_avg REAL,
            end_date TEXT,
            state TEXT,
            consecutive_no_blip_polls INTEGER DEFAULT 0,
            last_polled_at TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blip_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            condition_id TEXT,
            detected_at TEXT,
            trigger_type TEXT,
            volume_ratio REAL,
            price_delta REAL,
            hours_to_close REAL,
            outcome TEXT
        )
    ''')
