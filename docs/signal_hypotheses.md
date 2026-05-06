# Signal Hypotheses

## Phase 1: Blip Correlation Analysis

This document outlines hypotheses about pre-resolution trading signals in Polymarket prediction markets.

### Hypothesis 1: Volume Spike → Outcome Correlation

**Question**: Do markets with significant volume spikes in the final hours show a correlation between spike direction and resolution outcome?

**Expectation**: If YES-token volume spikes, the market is more likely to resolve YES (and vice versa).

**Metrics to Track**:
- Volume ratio at blip detection
- Time to resolution
- Outcome accuracy when volume spike occurs

### Hypothesis 2: Price Delta as Predictor

**Question**: Does a large price move always precede resolution, or only in certain categories?

**Expectation**: Politics and Crypto markets may show stronger price signals than Sports or Economics.

**Metrics to Track**:
- Price delta magnitude by category
- Signal accuracy by category
- False positive rate (no-blip markets that resolved one way)

### Hypothesis 3: Time Window Sensitivity

**Question**: Do blips within N hours of resolution have higher predictive power?

**Expectation**: Blips within 1–4 hours of close are more reliable than blips 24+ hours before.

**Metrics to Track**:
- Blip time-to-resolution distribution
- Signal accuracy as function of hours_to_close

---

## Phase 2 (Future): Real-Time Trading

Once Phase 1 correlations are validated, we can consider:
- Automated order placement on blip detection
- Risk management and position sizing
- Multi-market portfolio strategies
