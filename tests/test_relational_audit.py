"""Verify SQLite integration request/outcome records and parent links."""
import sqlite3
from app.providers.provider_record_request_audit import provider_record_request_audit
def test_integration_event_fk(tmp_path):
    path=str(tmp_path/"gateway.sqlite3")
    rid=provider_record_request_audit("POST","/process",200,2.8,path)
    with sqlite3.connect(path) as conn:
        assert conn.execute("SELECT COUNT(*) FROM integration_api_requests WHERE id=?",(rid,)).fetchone()[0]==1
        assert conn.execute("SELECT COUNT(*) FROM integration_api_events WHERE request_id=?",(rid,)).fetchone()[0]==1
        assert conn.execute("PRAGMA foreign_key_check").fetchall()==[]
