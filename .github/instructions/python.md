# Copilot Instructions for Python Files

## Core Principles

- **Python 3.11+** with explicit UTC datetimes
- **Type hints** on all function signatures
- **Docstrings** on all public functions: one-line summary + Args + Returns
- **No async/await** — synchronous polling with `time.sleep` is intentional
- **No pandas in scanner/** — only analyzer/ imports pandas
- **Never hardcode thresholds** — always reference `config.*`
- **All SQL in src/db/queries.py** — no inline SQL anywhere else

## Function Signature Example

```python
def detect_blip(
    condition_id: str,
    current_price: float,
    prev_price: float,
    volume_delta: float,
    prev_volume_avg: float,
    end_date: str,
) -> dict | None:
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
        Blip dict if triggered, None otherwise.
    """
```

## Error Handling in Polling Loop

Errors in individual market processing should be caught and logged, not propagated — a bad market should never kill the scan loop.

```python
try:
    result = process_market(market_id)
except Exception as e:
    print(f"[error] Market {market_id} failed: {e}")
    continue  # Move to next market
```

## Datetime Best Practices

- Always use `datetime` with explicit `timezone.utc`
- Never use naive datetimes
- Parse from ISO8601 strings: `datetime.fromisoformat("2025-05-06T10:30:00Z")`

```python
from datetime import datetime, timezone

now = datetime.now(timezone.utc)
end = datetime.fromisoformat("2025-12-31T23:59:59Z")
hours_remaining = (end - now).total_seconds() / 3600
```

## Domain Vocabulary

Use these terms consistently:

| Term | Meaning |
|------|--------|
| **market** | A Polymarket binary question (YES/NO resolution) |
| **condition_id** | Unique market identifier from Polymarket's Gamma API |
| **token_id** | YES-token identifier used in the CLOB order book |
| **blip** | A detected anomaly: volume spike and/or price delta |
| **blip event** | A persisted blip record with metadata |
| **state** | Market lifecycle: COLD → WARM → HOT → RESOLVED |
| **volume_ratio** | current_volume_delta / rolling_avg_volume |
| **price_delta** | Absolute price change since last poll, range 0.0–1.0 |
| **hours_to_close** | Time remaining until market resolution |
| **outcome** | "Yes" or "No" — the resolved binary outcome |

## Config Reference

Always reference these from `config.py`:

```python
import config

# Thresholds
VOLUME_SPIKE = config.VOLUME_SPIKE_MULTIPLIER
PRICE_DELTA = config.PRICE_DELTA_THRESHOLD

# Poll intervals
COLD_FREQ = config.POLL_INTERVAL_COLD
WARM_FREQ = config.POLL_INTERVAL_WARM
HOT_FREQ = config.POLL_INTERVAL_HOT

# Database
db_path = config.DB_PATH
```

## API Rate Limiting

- Always sleep 50–100ms between API calls
- Use `time.sleep(random.uniform(config.API_MIN_SLEEP, config.API_MAX_SLEEP))`
- No authentication required for read-only endpoints

## Testing

- Use pytest
- Fixtures in `tests/fixtures/`
- Mock API responses, don't call live endpoints in tests
