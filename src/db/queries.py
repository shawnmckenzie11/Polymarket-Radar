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
    end_date: str,
    state: str,
) -> None:
    """
    Upsert a market record (INSERT ... ON CONFLICT DO UPDATE).

    Args:
        conn: Database connection.
        condition_id: Market identifier.
        category: Market category (Politics, Crypto, etc.).
        question: Full market question text.
        current_price: Current YES-token price.
        end_date: ISO8601 market close time.
        state: Current state (COLD, WARM, HOT, RESOLVED).
    """
    # TODO: Implement upsert
    pass


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

    Args:
        conn: Database connection.
        condition_id: Market identifier.
        detected_at: Blip detection timestamp (UTC).
        trigger_type: "volume", "price", or "both".
        volume_ratio: Current volume / rolling average.
        price_delta: Absolute price change.
        hours_to_close: Time to market resolution.
    """
    # TODO: Implement insert
    pass


def get_market_state(
    conn: sqlite3.Connection,
    condition_id: str,
) -> Optional[dict]:
    """
    Fetch current market state and metadata.

    Args:
        conn: Database connection.
        condition_id: Market identifier.

    Returns:
        Market dict or None if not found.
    """
    # TODO: Implement select
    pass


def backfill_outcomes(
    conn: sqlite3.Connection,
    condition_id: str,
    outcome: str,
) -> None:
    """
    Backfill outcome for all blip_events matching a resolved market.

    Args:
        conn: Database connection.
        condition_id: Market identifier.
        outcome: "Yes" or "No".
    """
    # TODO: Implement UPDATE to set blip_events.outcome where market matches
    pass
