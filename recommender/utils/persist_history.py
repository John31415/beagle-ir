import sqlite3
from datetime import datetime

def add_query(query: str, dt: datetime, db_path: str):
    with sqlite3.connect(db_path) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS history (query TEXT, timestamp TEXT)''')
        conn.execute('INSERT INTO history (query, timestamp) VALUES (?, ?)', (query, dt.isoformat()))

def get_all_queries(db_path: str) -> list[tuple[str, str]]:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute('SELECT query, timestamp FROM history')
        return cursor.fetchall()