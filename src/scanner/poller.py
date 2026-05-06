"""
Wide market poller.

Scans Polymarket for new and active markets, manages polling frequency
by market state (COLD, WARM, HOT, RESOLVED), and delegates blip detection.
"""

import time
import requests
from datetime import datetime, timezone

import config
from src.db.schema import init_database
from src.db.queries import get_market_state, upsert_market, insert_blip_event
from src.scanner.detector import detect_blip
from src.scanner.state import transition_state


def fetch_active_markets() -> list:
    """Fetch active markets from Gamma API."""
    try:
        url = f"{config.GAMMA_API_BASE}/events"
        params = {"active": "true", "closed": "false", "limit": config.MARKETS_PAGE_SIZE}
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"[poller] Error fetching Gamma API: {e}")
        return []


def poll_all_markets() -> None:
    """
    Main polling loop: fetch markets, check state, poll at appropriate frequency.
    
    Runs indefinitely. Errors in individual market processing are logged and
    do not propagate — the loop continues.
    """
    print("[poller] Starting market scan...")
    conn = init_database()
    
    while True:
        try:
            # 1. Fetch active markets from Gamma API
            markets_data = fetch_active_markets()
            
            for event in markets_data:
                markets = event.get("markets", []) if "markets" in event else [event]
                for market in markets:
                    condition_id = market.get("conditionId") or market.get("id")
                    if not condition_id:
                        continue
                        
                    # 2. Load market states from database
                    db_state = get_market_state(conn, condition_id)
                    current_state = db_state.get("state", "COLD") if db_state else "COLD"
                    last_polled_str = db_state.get("last_polled_at") if db_state else None
                    
                    # 3. For each market, check if poll interval has elapsed
                    interval = config.POLL_INTERVAL_COLD
                    if current_state == "WARM":
                        interval = config.POLL_INTERVAL_WARM
                    elif current_state == "HOT":
                        interval = config.POLL_INTERVAL_HOT
                    elif current_state == "RESOLVED":
                        continue
                    
                    now = datetime.now(timezone.utc)
                    if last_polled_str:
                        try:
                            last_polled_at = datetime.fromisoformat(last_polled_str.replace("Z", "+00:00"))
                            elapsed = (now - last_polled_at).total_seconds()
                            if elapsed < interval:
                                continue
                        except ValueError:
                            pass
                    
                    # 4. If yes, poll CLOB/price data, run detector, update state
                    current_price = 0.5
                    tokens = market.get("tokens", [])
                    if tokens and isinstance(tokens, list) and len(tokens) > 0:
                        current_price = float(tokens[0].get("price", current_price))
                        
                    prev_price = db_state.get("current_price", current_price) if db_state else current_price
                    prev_volume_avg = db_state.get("rolling_volume_avg", 500.0) if db_state else 500.0
                    
                    volume_delta = float(market.get("volume24hr", 0.0))
                    end_date = market.get("endDate", "")
                    
                    blip = detect_blip(
                        condition_id=condition_id,
                        current_price=current_price,
                        prev_price=prev_price,
                        volume_delta=volume_delta,
                        prev_volume_avg=prev_volume_avg,
                        end_date=end_date
                    )
                    
                    consec_no_blip = db_state.get("consecutive_no_blip_polls", 0) if db_state else 0
                    if blip:
                        consec_no_blip = 0
                    else:
                        consec_no_blip += 1
                        
                    market_closed = market.get("closed", False)
                    
                    next_state = transition_state(
                        current_state=current_state,
                        blip_detected=blip is not None,
                        consecutive_no_blip_polls=consec_no_blip,
                        market_closed=market_closed,
                        blip=blip
                    )
                    
                    if blip:
                        insert_blip_event(
                            conn=conn,
                            condition_id=condition_id,
                            detected_at=now,
                            trigger_type=blip.get("trigger_type", "unknown"),
                            volume_ratio=blip.get("volume_ratio", 0.0),
                            price_delta=blip.get("price_delta", 0.0),
                            hours_to_close=blip.get("hours_to_close", 0.0)
                        )
                    
                    upsert_market(
                        conn=conn,
                        condition_id=condition_id,
                        category=event.get("category", "Unknown"),
                        question=market.get("question", "Unknown"),
                        current_price=current_price,
                        end_date=end_date,
                        state=next_state
                    )
                    
                    if config.VERBOSE_POLLING:
                        # Log if ID looks unusual (e.g., short integer ID instead of hex hash)
                        if not condition_id.startswith("0x") or len(condition_id) < 60:
                            print(f"[poller] NON-STANDARD ID DETECTED: {condition_id} | {current_state} -> {next_state} | Price: {current_price}")
                        else:
                            print(f"[poller] {condition_id} | {current_state} -> {next_state} | Price: {current_price}")
                        
                    time.sleep(config.API_MIN_SLEEP)
                    
        except Exception as e:
            print(f"[poller] Error in polling loop: {e}")
            
        # 5. Sleep and repeat
        if config.VERBOSE_POLLING:
            print("[poller] Cycle complete. Sleeping...")
        time.sleep(10)


if __name__ == "__main__":
    poll_all_markets()
