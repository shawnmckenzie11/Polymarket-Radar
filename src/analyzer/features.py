"""
Signal feature extraction.

Computes derived features from raw market and blip data for correlation analysis.
"""

from typing import Optional
import config

def simulate_detector(history: list) -> Optional[dict]:
    """
    Run blip detection logic over historical timeseries.
    Returns the last detected blip before the end of the timeseries, or None.
    """
    last_blip = None
    
    # We need to simulate a rolling average. Let's use a simple window of 5 periods
    for i in range(5, len(history)):
        current_pt = history[i]
        prev_pt = history[i-1]
        
        current_price = current_pt.get("p", 0.0)
        prev_price = prev_pt.get("p", 0.0)
        
        # Approximate volume from prices/timestamps isn't possible from CLOB 'p' alone
        # if there's no volume data. Wait, CLOB prices-history usually has 'p' and 't'.
        # If there's no volume, we can only test the price delta hypothesis on this historical data.
        price_delta = abs(current_price - prev_price)
        
        if price_delta >= config.PRICE_DELTA_THRESHOLD:
            # We found a price blip
            # time to resolution is the difference between the final point and this point
            final_time = history[-1].get("t", current_pt.get("t"))
            current_time = current_pt.get("t")
            hours_to_close = (final_time - current_time) / 3600.0
            
            last_blip = {
                "trigger_type": "price",
                "price_delta": price_delta,
                "volume_ratio": 0.0, # Not available in basic CLOB history
                "hours_to_close": hours_to_close,
                "price_direction": "UP" if current_price > prev_price else "DOWN",
                "detected_at_idx": i
            }
            
    return last_blip

def extract_blip_features(market_data: dict) -> Optional[dict]:
    """
    Extract analysis features from a historical market timeseries.

    Args:
        market_data: Dict with condition_id, question, winning_outcome, history

    Returns:
        Feature dict for correlation analysis, or None if no blip found.
    """
    history = market_data.get("history", [])
    if len(history) < 5:
        return None
        
    blip = simulate_detector(history)
    if not blip:
        return None
        
    # Return enriched features
    return {
        "condition_id": market_data["condition_id"],
        "question": market_data.get("question", "Unknown"),
        "category": market_data["category"],
        "winning_outcome": market_data["winning_outcome"],
        "trigger_type": blip["trigger_type"],
        "price_delta": blip["price_delta"],
        "hours_to_close": blip["hours_to_close"],
        "price_direction": blip["price_direction"]
    }
