import os
import json
import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Ensure project root is on sys.path for imports when running tests
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.main import app
from app.database import init_db

# Ensure DB tables exist and sample data loaded for tests
init_db()

client = TestClient(app)


def test_health():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_read_stations():
    r = client.get("/stations/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_crud_station():
    # create
    payload = {"title": "Test Station", "town": "Testtown", "country": "TS", "lat": 10.0, "lon": 20.0}
    r = client.post("/stations/", json=payload)
    assert r.status_code == 201
    data = r.json()
    station_id = data["id"] if isinstance(data, dict) and "id" in data else data.get('id')
    assert station_id is not None

    # read
    r = client.get(f"/stations/{station_id}")
    assert r.status_code == 200
    assert r.json()["title"] == "Test Station"

    # update
    r = client.put(f"/stations/{station_id}", json={"title": "Updated"})
    assert r.status_code == 200
    assert r.json()["title"] == "Updated"

    # delete
    r = client.delete(f"/stations/{station_id}")
    assert r.status_code == 204

    # ensure gone
    r = client.get(f"/stations/{station_id}")
    assert r.status_code == 404


def test_analytics_endpoints():
    r = client.get("/analytics/count")
    assert r.status_code == 200
    assert "count" in r.json()

    # by operator (may be empty)
    r2 = client.get("/analytics/by_operator", params={"operator": "Electra"})
    assert r2.status_code == 200
