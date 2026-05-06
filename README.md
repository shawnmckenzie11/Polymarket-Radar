# Polymarket Radar

**A blip detection system for Polymarket prediction markets.**

This project scans Polymarket binary markets for sudden spikes in trading volume or price delta that precede market resolution. The goal is to identify whether these pre-resolution signals ("blips") correlate with YES/NO outcomes across categories like Politics, Crypto, Economics, and Sports.

## Architecture

```
polymarket-radar/
├── src/
│   ├── scanner/          # Market polling + state machine
│   │   ├── poller.py     # Wide slow scan of all markets
│   │   ├── detector.py   # Blip detection logic
│   │   └── state.py      # COLD → WARM → HOT → RESOLVED transitions
│   ├── analyzer/         # Phase 1: retrospective analysis
│   │   ├── features.py   # Signal feature extraction
│   │   ├── correlator.py # Blip → outcome correlation
│   │   └── plots.py      # Matplotlib visualizations
│   └── db/
│       ├── schema.py     # SQLite schema definitions
│       └── queries.py    # All DB reads/writes (no inline SQL elsewhere)
├── tests/
│   ├── test_detector.py
│   ├── test_features.py
│   └── fixtures/         # Sample API response JSON
├── docs/
│   └── signal_hypotheses.md
├── .github/
│   └── instructions/     # Per-file-type Copilot instructions
└── config.py             # All thresholds live here — never hardcode
```

## Quick Start

1. Clone the repository
2. Create a virtual environment: `python3.11 -m venv venv`
3. Activate: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Configure thresholds in `config.py`
6. Run the scanner: `python -m src.scanner.poller`

## Core Concepts

- **Market**: A Polymarket binary question (YES/NO resolution)
- **Blip**: An anomaly detected—volume spike and/or price delta crossing threshold
- **State**: Market lifecycle: `COLD` → `WARM` → `HOT` → `RESOLVED`
- **Volume Ratio**: Current volume delta / rolling average volume (primary blip trigger)
- **Price Delta**: Absolute price change since last poll
- **Hours to Close**: Time remaining until market resolution at blip detection
- **Outcome**: `"Yes"` or `"No"` — the resolved binary outcome

## APIs

### Gamma API — Market metadata
- Base: `https://gamma-api.polymarket.com`
- `/markets` — list markets
- `/markets/{condition_id}` — single market detail
- `/prices-history` — OHLCV price series

### CLOB API — Order book and trades
- Base: `https://clob.polymarket.com`
- `/book` — current order book
- `/trades` — recent trades

**Note**: Always sleep 50–100ms between API calls. No authentication required for read-only endpoints.

## Development

- Python 3.11+
- Type hints on all functions
- All SQL lives in `src/db/queries.py`
- All thresholds/intervals in `config.py` — never hardcode
- Synchronous polling with `time.sleep` (no async/await)

## License

MIT
