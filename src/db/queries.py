"""
Database queries: all reads and writes.

No inline SQL anywhere else in the codebase. All database operations
should go through these functions.
"""

import sqlite3
from typing import Optional
from datetime import datetime, timezone


def upsert_market(
    conn: sqlite3.Connection,
    condition_id: str,
    category: str,
    question: str,
    current_price: float,
    rolling_volume_avg: float,
    consecutive_no_blip_polls: int,
    end_date: str,
    state: str,
    last_polled_at: str,
) -> None:
    """
    Upsert a market record (INSERT ... ON CONFLICT DO UPDATE).
    """
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO markets (
            condition_id, category, question, current_price, rolling_volume_avg,
            consecutive_no_blip_polls, end_date, state, last_polled_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(condition_id) DO UPDATE SET
            category=excluded.category,
            question=excluded.question,
            current_price=excluded.current_price,
            rolling_volume_avg=excluded.rolling_volume_avg,
            consecutive_no_blip_polls=excluded.consecutive_no_blip_polls,
            end_date=excluded.end_date,
            state=excluded.state,
            last_polled_at=excluded.last_polled_at
    ''', (condition_id, category, question, current_price, rolling_volume_avg,
          consecutive_no_blip_polls, end_date, state, last_polled_at))
    conn.commit()


def insert_blip_event(
    conn: sqlite3.Connection,
    condition_id: str,
    detected_at: datetime,
    trigger_type: str,
    volume_ratio: float,
    price_delta: float,
    hours_to_close: float,
) -> None:
    """
    Insert a new blip event.
    """
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO blip_events (
            condition_id, detected_at, trigger_type, volume_ratio, 
            price_delta, hours_to_close
        ) VALUES (?, ?, ?, ?, ?, ?)
    ''', (condition_id, detected_at.isoformat(), trigger_type, volume_ratio, 
          price_delta, hours_to_close))
    conn.commit()


def get_market_state(
    conn: sqlite3.Connection,
    condition_id: str,
) -> Optional[dict]:
    """
    Fetch current market state and metadata.
    """
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM markets WHERE condition_id = ?', (condition_id,))
    row = cursor.fetchone()
    
    if not row:
        return None
        
    cols = [col[0] for col in cursor.description]
    return dict(zip(cols, row))


def backfill_outcomes(
    conn: sqlite3.Connection,
    condition_id: str,
    outcome: str,
) -> None:
    """
    Backfill outcome for all blip_events matching a resolved market.
    """
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE blip_events SET outcome = ? WHERE condition_id = ?
    ''', (outcome, condition_id))
    conn.commit()
