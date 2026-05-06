"""
Central configuration for Polymarket Radar.

All thresholds, intervals, and API parameters are defined here.
Never hardcode these values — always reference config.*
"""

import os
from datetime import timedelta

# ============================================================================
# API Configuration
# ============================================================================

GAMMA_API_BASE = "https://gamma-api.polymarket.com"
CLOB_API_BASE = "https://clob.polymarket.com"

# Minimum sleep between API calls (seconds)
API_MIN_SLEEP = 0.05  # 50ms minimum
API_MAX_SLEEP = 0.1   # 100ms maximum

# ============================================================================
# Market Scanning Configuration
# ============================================================================

# Markets per page when fetching from Gamma API
MARKETS_PAGE_SIZE = 100

# Categories to scan (None = scan all)
CATEGORIES_TO_SCAN = None  # Options: "Politics", "Crypto", "Economics", "Sports"

# ============================================================================
# State Machine: Poll Frequency (seconds)
# ============================================================================

# COLD markets: wide, infrequent scan
POLL_INTERVAL_COLD = 4 * 60 * 60  # 4 hours

# WARM markets: elevated attention
POLL_INTERVAL_WARM = 5 * 60  # 5 minutes

# HOT markets: lock-on behavior
POLL_INTERVAL_HOT = 1 * 60  # 1 minute

# ============================================================================
# Blip Detection Thresholds
# ============================================================================

# Volume-based trigger: volume_ratio = current_delta / rolling_avg
VOLUME_SPIKE_MULTIPLIER = 5.0  # 5x rolling average triggers WARM

# Price-based trigger: absolute delta since last poll
PRICE_DELTA_THRESHOLD = 0.05  # 5% price move triggers WARM

# Dual trigger: both volume AND price spikes → HOT
BOTH_TRIGGERS_THRESHOLD = True  # If True, both must spike simultaneously

# Cooldown: drop back to WARM if triggers absent for N polls
WARM_TO_COLD_COOLDOWN_POLLS = 2  # 2 consecutive polls without signal

# ============================================================================
# Database Configuration
# ============================================================================

DB_PATH = os.getenv("POLYMARKET_DB_PATH", "polymarket_radar.db")

# ============================================================================
# Logging & Debugging
# ============================================================================

# Set to True to print detailed polling info
VERBOSE_POLLING = True

# ============================================================================
# Phase 1: Analyzer Configuration
# ============================================================================

# Rolling window for volume averaging (hours)
ROLLING_WINDOW_HOURS = 24

# Minimum blip events to include in correlation analysis
MIN_BLIPS_FOR_ANALYSIS = 5
