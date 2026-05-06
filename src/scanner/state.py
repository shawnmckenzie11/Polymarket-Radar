"""
Market state machine.

Manages transitions: COLD → WARM → HOT → RESOLVED
based on blip detection and cooldown logic.
"""

from typing import Literal, Optional

import config

MarketState = Literal["COLD", "WARM", "HOT", "RESOLVED"]


def transition_state(
    current_state: MarketState,
    blip_detected: bool,
    consecutive_no_blip_polls: int,
    market_closed: bool,
    blip: Optional[dict] = None,
    settings: dict = None,
) -> MarketState:
    """
    Determine next market state based on detection and cooldown logic.

    Args:
        current_state: Current state (COLD, WARM, HOT, RESOLVED).
        blip_detected: True if detector returned a blip.
        consecutive_no_blip_polls: Count of polls without blip in WARM/HOT.
        market_closed: True if market.closed == True.
        blip: The full blip dictionary if blip_detected is True.
        settings: Database settings dictionary.

    Returns:
        Next state.
    """
    settings = settings or {}
    both_trig = settings.get("BOTH_TRIGGERS_THRESHOLD", str(config.BOTH_TRIGGERS_THRESHOLD)).lower() == "true"
    cooldown_polls = int(settings.get("WARM_TO_COLD_COOLDOWN_POLLS", config.WARM_TO_COLD_COOLDOWN_POLLS))

    if market_closed:
        return "RESOLVED"
        
    if current_state == "RESOLVED":
        return "RESOLVED"
        
    if current_state == "COLD":
        if blip_detected:
            return "WARM"
        return "COLD"
        
    if current_state == "WARM":
        if blip_detected:
            # Check if we should transition to HOT
            if both_trig:
                trigger = blip.get("trigger_type") if blip else None
                if trigger == "both":
                    return "HOT"
                else:
                    return "WARM"
            else:
                return "HOT"
        else:
            if consecutive_no_blip_polls >= cooldown_polls:
                return "COLD"
            return "WARM"
            
    if current_state == "HOT":
        if not blip_detected:
            if consecutive_no_blip_polls >= cooldown_polls:
                return "WARM"
        return "HOT"

    return current_state
