"""
Wide market poller.

Scans Polymarket for new and active markets, manages polling frequency
by market state (COLD, WARM, HOT, RESOLVED), and delegates blip detection.
"""

import time
from datetime import datetime, timezone

import config


def poll_all_markets() -> None:
    """
    Main polling loop: fetch markets, check state, poll at appropriate frequency.
    
    Runs indefinitely. Errors in individual market processing are logged and
    do not propagate — the loop continues.
    """
    print("[poller] Starting market scan...")
    # TODO: Implement main polling loop
    # 1. Fetch active markets from Gamma API
    # 2. Load market states from database
    # 3. For each market, check if poll interval has elapsed
    # 4. If yes, poll CLOB/price data, run detector, update state
    # 5. Sleep and repeat
    pass


if __name__ == "__main__":
    poll_all_markets()
