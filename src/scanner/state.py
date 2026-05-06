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
) -> MarketState:
    """
    Determine next market state based on detection and cooldown logic.

    Args:
        current_state: Current state (COLD, WARM, HOT, RESOLVED).
        blip_detected: True if detector returned a blip.
        consecutive_no_blip_polls: Count of polls without blip in WARM/HOT.
        market_closed: True if market.closed == True.
        blip: The full blip dictionary if blip_detected is True.

    Returns:
        Next state.
    """
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
            if config.BOTH_TRIGGERS_THRESHOLD:
                # Require both triggers if config says so, but our detector handles returning a blip based on config.
                # However, if detector returns a blip with 'volume' and BOTH_TRIGGERS is True, wait, detector wouldn't
                # return it if BOTH_TRIGGERS_THRESHOLD was true unless it was 'both'. 
                # Let's just transition to HOT if we get another blip, or if the blip has trigger_type == 'both'.
                trigger = blip.get("trigger_type") if blip else None
                if trigger == "both":
                    return "HOT"
                else:
                    return "WARM"
            else:
                return "HOT"
        else:
            if consecutive_no_blip_polls >= config.WARM_TO_COLD_COOLDOWN_POLLS:
                return "COLD"
            return "WARM"
            
    if current_state == "HOT":
        if not blip_detected:
            if consecutive_no_blip_polls >= config.WARM_TO_COLD_COOLDOWN_POLLS:
                return "WARM"
        return "HOT"

    return current_state
