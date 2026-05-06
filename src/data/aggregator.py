"""
Signal aggregator: combines Gamma + Goldsky + Probalytics into unified feature set.

Phase 1: Gamma API only (baseline).
Phase 2: Add Goldsky order fills (informed positioning) + Probalytics spreads (microstructure).
"""

from typing import Optional, dict
from datetime import datetime, timezone

import config
from src.data.providers import DataProviderFactory


class SignalAggregator:
    """
    Unified feature computation layer.
    
    Automatically selects data sources based on availability.
    Falls back gracefully if a provider is disabled.
    """

    def __init__(self):
        """Initialize aggregator with available providers."""
        self.providers = DataProviderFactory.get_all_providers()
        self.gamma = self.providers["gamma"]
        self.goldsky = self.providers["goldsky"]
        self.probalytics = self.providers["probalytics"]

    def compute_market_features(
        self,
        condition_id: str,
        lookback_hours: int = 24,
    ) -> dict:
        """
        Compute comprehensive feature set for a market.

        Combines:
        - Gamma API: price, volume, liquidity
        - Goldsky (if enabled): informed trader positioning
        - Probalytics (if enabled): spread + depth microstructure

        Args:
            condition_id: Market condition ID.
            lookback_hours: Analysis window.

        Returns:
            Feature dict with all available signals.
        """
        features = {
            "condition_id": condition_id,
            "computed_at": datetime.now(timezone.utc).isoformat(),
            "lookback_hours": lookback_hours,
        }

        # ===== Gamma API: Baseline signals (always available) =====
        if self.gamma.is_available():
            gamma_features = self._compute_gamma_features(condition_id, lookback_hours)
            features.update(gamma_features)

        # ===== Goldsky: Informed trader positioning (Phase 2+) =====
        if self.goldsky.is_available() and config.USE_GOLDSKY_FILLS:
            goldsky_features = self._compute_goldsky_features(
                condition_id, lookback_hours
            )
            features.update(goldsky_features)

        # ===== Probalytics: Spread + depth microstructure (Phase 2+) =====
        if self.probalytics.is_available() and config.USE_PROBALYTICS_SPREADS:
            probalytics_features = self._compute_probalytics_features(
                condition_id, lookback_hours
            )
            features.update(probalytics_features)

        return features

    def _compute_gamma_features(
        self,
        condition_id: str,
        lookback_hours: int,
    ) -> dict:
        """
        Compute features from Gamma API.

        Returns:
            Dict with keys:
            - gamma_price: Current YES-token price
            - gamma_volume_24h: 24-hour trading volume
            - gamma_liquidity: Total liquidity
            - gamma_price_change_24h: Price % change
            - gamma_volatility: Price volatility
        """
        # TODO: Implement
        # 1. Fetch price history from Gamma
        # 2. Compute rolling volatility, volume aggregates
        # 3. Return feature dict
        pass

    def _compute_goldsky_features(
        self,
        condition_id: str,
        lookback_hours: int,
    ) -> dict:
        """
        Compute features from Goldsky order-filled events.

        Returns:
            Dict with keys:
            - goldsky_whale_bias: "yes", "no", or "balanced"
            - goldsky_whale_volume_yes: Total large YES orders (USD)
            - goldsky_whale_volume_no: Total large NO orders (USD)
            - goldsky_fill_velocity: Orders per minute
            - goldsky_informed_score: 0–1 confidence in informed positioning
        """
        # TODO: Implement
        # 1. Fetch order fills from Goldsky
        # 2. Identify whale orders (size > threshold)
        # 3. Compute positioning metrics
        # 4. Return feature dict
        pass

    def _compute_probalytics_features(
        self,
        condition_id: str,
        lookback_hours: int,
    ) -> dict:
        """
        Compute features from Probalytics orderbook data.

        Returns:
            Dict with keys:
            - probalytics_avg_spread: Average bid-ask spread (%)
            - probalytics_spread_trend: Is spread widening or tightening?
            - probalytics_depth_imbalance: Current order book imbalance (-1 to +1)
            - probalytics_depth_imbalance_trend: Is imbalance increasing/decreasing?
            - probalytics_microstructure_score: 0–1 strength of market conviction
        """
        # TODO: Implement
        # 1. Query ClickHouse for orderbook snapshots
        # 2. Compute spread timeseries + depth imbalance
        # 3. Compute trend indicators
        # 4. Return feature dict
        pass

    def compute_blip_correlation_features(
        self,
        blip_event: dict,
    ) -> dict:
        """
        Compute additional enriched features for a detected blip.

        Used by Phase 1 analyzer to correlate blips with outcomes.

        Args:
            blip_event: Blip record with trigger_type, volume_ratio, hours_to_close, etc.

        Returns:
            Enhanced feature dict including informed trader signals + microstructure.
        """
        # TODO: Implement
        # 1. Extract condition_id, detected_at from blip
        # 2. Compute market features at time of blip
        # 3. Add correlation features (outcome likelihood, etc.)
        # 4. Return enriched dict
        pass
