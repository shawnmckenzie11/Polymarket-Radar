from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os

from src.db.schema import init_database
from src.db.queries import get_active_markets, get_recent_blips
import config

app = FastAPI(title="Polymarket Radar API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    conn = init_database()
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/api/markets")
def api_get_markets():
    conn = get_db()
    try:
        markets = get_active_markets(conn)
        return {"status": "success", "data": markets}
    finally:
        conn.close()

@app.get("/api/blips")
def api_get_blips():
    conn = get_db()
    try:
        blips = get_recent_blips(conn, limit=50)
        return {"status": "success", "data": blips}
    finally:
        conn.close()

# Mount static files for the frontend dashboard
# We will place our frontend in a folder called 'public' at the root
public_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "public")
os.makedirs(public_dir, exist_ok=True)

app.mount("/", StaticFiles(directory=public_dir, html=True), name="public")
