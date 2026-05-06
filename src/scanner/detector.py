"""
Blip detection logic.

Evaluates whether a market crosses volume and/or price thresholds
to trigger a blip event and state transition.
"""

from typing import Optional
from datetime import datetime, timezone
import dateutil.parser

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
    volume_ratio = volume_delta / prev_volume_avg if prev_volume_avg > 0 else 0.0
    price_delta = abs(current_price - prev_price)
    
    vol_spike = volume_ratio >= config.VOLUME_SPIKE_MULTIPLIER
    price_spike = price_delta >= config.PRICE_DELTA_THRESHOLD
    
    trigger_type = None
    if vol_spike and price_spike:
        trigger_type = "both"
    elif vol_spike and not config.BOTH_TRIGGERS_THRESHOLD:
        trigger_type = "volume"
    elif price_spike and not config.BOTH_TRIGGERS_THRESHOLD:
        trigger_type = "price"
        
    if trigger_type:
        hours_to_close = -1.0
        if end_date:
            try:
                ed = dateutil.parser.isoparse(end_date)
                if ed.tzinfo is None:
                    ed = ed.replace(tzinfo=timezone.utc)
                now = datetime.now(timezone.utc)
                hours_to_close = max(0.0, (ed - now).total_seconds() / 3600.0)
            except Exception:
                pass

        return {
            "trigger_type": trigger_type,
            "price_delta": price_delta,
            "volume_ratio": volume_ratio,
            "hours_to_close": hours_to_close
        }
        
    return None
