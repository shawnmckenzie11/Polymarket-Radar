"""
Market state machine.

Manages transitions: COLD → WARM → HOT → RESOLVED
based on blip detection and cooldown logic.
"""

from typing import Literal

import config

MarketState = Literal["COLD", "WARM", "HOT", "RESOLVED"]


def transition_state(
    current_state: MarketState,
    blip_detected: bool,
    consecutive_no_blip_polls: int,
    market_closed: bool,
) -> MarketState:
    """
    Determine next market state based on detection and cooldown logic.

    Args:
        current_state: Current state (COLD, WARM, HOT, RESOLVED).
        blip_detected: True if detector returned a blip.
        consecutive_no_blip_polls: Count of polls without blip in WARM/HOT.
        market_closed: True if market.closed == True.

    Returns:
        Next state.
    """
    # TODO: Implement state machine transitions
    # COLD + blip → WARM
    # WARM + both_triggers → HOT
    # WARM + cooldown_reached → COLD
    # ANY + market_closed → RESOLVED
    pass
