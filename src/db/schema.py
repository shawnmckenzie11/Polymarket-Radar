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

    # TODO: Create all tables
    # - markets (condition_id, category, question, current_price, end_date, state, last_polled_at, ...)
    # - snapshots (market_id, polled_at, price, volume_24h, ...)
    # - blip_events (market_id, detected_at, trigger_type, volume_ratio, price_delta, hours_to_close, outcome, ...)

    conn.commit()
    return conn


def create_tables(cursor: sqlite3.Cursor) -> None:
    """
    Create all required tables.

    Args:
        cursor: SQLite cursor.
    """
    # TODO: Implement CREATE TABLE statements
    pass
