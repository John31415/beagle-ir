import sqlite3
from datetime import datetime
from pathlib import Path

DEFAULT_HISTORY_DB = Path(__file__).resolve().parents[0] / "history.db"

def add_query(query: str, dt: datetime, db_path = DEFAULT_HISTORY_DB) -> None:
    cleaned_query = query.strip()
    if not cleaned_query:
        return
    with sqlite3.connect(db_path) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS history (query TEXT, timestamp TEXT)")
        conn.execute(
            "INSERT INTO history (query, timestamp) VALUES (?, ?)",
            (cleaned_query, dt.isoformat()),
        )

def get_all_queries(db_path = DEFAULT_HISTORY_DB) -> list[tuple[str, str]]:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute("SELECT query, timestamp FROM history ORDER BY timestamp DESC")
        return cursor.fetchall()