"""
Blip detection logic.

Evaluates whether a market crosses volume and/or price thresholds
to trigger a blip event and state transition.
"""

from typing import Optional

import config


def detect_blip(
    condition_id: str,
    current_price: float,
    prev_price: float,
    volume_delta: float,
    prev_volume_avg: float,
    end_date: str,
) -> Optional[dict]:
    """
    Evaluate whether current market state crosses blip detection thresholds.

    Args:
        condition_id: Polymarket condition identifier.
        current_price: Current YES-token price (0.0–1.0).
        prev_price: Price at last poll.
        volume_delta: Volume traded since last poll.
        prev_volume_avg: Rolling average volume for ratio baseline.
        end_date: ISO8601 market close time.

    Returns:
        Blip dict with keys (trigger_type, price_delta, volume_ratio, hours_to_close)
        if thresholds crossed, None otherwise.
    """
    # TODO: Implement blip detection
    # 1. Calculate volume_ratio = volume_delta / prev_volume_avg
    # 2. Calculate price_delta = abs(current_price - prev_price)
    # 3. Check thresholds from config
    # 4. Return blip dict or None
    pass
