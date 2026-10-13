"""SQLite persistence for privacy-safe integration API requests and outcome events."""
import os
import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4

def provider_record_request_audit(method: str, route: str, status: int, duration_ms: float, database_path: str | None = None) -> str:
    """Store request and linked outcome; never store query bodies or credentials."""
    path = database_path or os.getenv("INKPLAIN_AUDIT_DB", "data/integration_audit.sqlite3")
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    identifier = uuid4().hex
    timestamp = datetime.now(timezone.utc).isoformat()
    with sqlite3.connect(path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("""CREATE TABLE IF NOT EXISTS integration_api_requests (
            id TEXT PRIMARY KEY,
            route TEXT NOT NULL,
            method TEXT NOT NULL,
            created_at TEXT NOT NULL
        )""")
        connection.execute("""CREATE TABLE IF NOT EXISTS integration_api_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id TEXT NOT NULL REFERENCES integration_api_requests(id),
            http_status INTEGER NOT NULL,
            duration_ms REAL NOT NULL,
            occurred_at TEXT NOT NULL
        )""")
        connection.execute("INSERT INTO integration_api_requests (id, route, method, created_at) VALUES (?, ?, ?, ?)", (identifier, route, method, timestamp))
        connection.execute("INSERT INTO integration_api_events (request_id, http_status, duration_ms, occurred_at) VALUES (?, ?, ?, ?)", (identifier, int(status), round(duration_ms, 2), timestamp))
    return identifier
