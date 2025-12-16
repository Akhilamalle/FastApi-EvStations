<<<<<<< HEAD
# EV Stations FastAPI

This repository provides a small FastAPI service that exposes a dataset of electric vehicle (EV) charging
stations (bundled as CSV) through a REST API. The app uses SQLAlchemy with a local SQLite database by
default and includes small analytics endpoints with summary and geo-distance helpers.

Contents (consolidated)

- Setup & Usage
- API Reference
- Dataset description
- Testing & Notes

----

**Setup & Usage**

Requirements

- Python 3.9+ (3.10/3.11 recommended)
- Install dependencies from `requirements.txt` (FastAPI, uvicorn, SQLAlchemy, pydantic, pytest...)

Installation

1. Create and activate a virtualenv:

```bash
python -m venv .venv
# Unix/macOS
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Windows (cmd.exe)
.venv\Scripts\activate.bat
```

2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run locally

```bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for interactive API docs (Swagger UI).

Database & dataset

- Default DB: SQLite using `sqlite:///./ev_stations.db` (see `app/database.py`).
- On startup `init_db()` creates tables and loads `app/data/ev_stations_2025.csv` into the `ev_stations` table
  if it is empty.
- To use a different DB set `DATABASE_URL` environment variable, e.g.:

```bash
export DATABASE_URL="postgresql+psycopg2://user:pass@host:5432/dbname"
# Windows (PowerShell)
$env:DATABASE_URL = 'postgresql+psycopg2://user:pass@host:5432/dbname'
```

Notes

- CSV loading is tolerant: malformed numeric or datetime fields become `NULL`.
- The `nearest` endpoint uses a Python Haversine calculation; for large datasets use a spatial index (PostGIS).

----

**API Reference**

Base URL (local): `http://127.0.0.1:8000`

All endpoints are discoverable at `/docs` when the server runs.

Health

- `GET /healthz` — returns `{ "status": "ok" }`.

Stations router (`/stations`)

- `GET /stations/` — list stations
  - Query: `skip` (int, default 0), `limit` (int, default 100)
- `GET /stations/{id}` — get station by id (404 if not found)
- `POST /stations/` — create station; body: `EVStationCreate` (partial allowed)
- `PUT /stations/{id}` — update station; body: `EVStationUpdate`
- `DELETE /stations/{id}` — delete station (204)

Station JSON (example)

```json
{
  "id": 462769,
  "title": "Electra - Wambrechies - Volfoni",
  "address": "81 Av. Clément Ader",
  "town": "Wambrechies",
  "state": "",
  "postcode": "59118",
  "country": "FR",
  "lat": 50.68565,
  "lon": 3.06241,
  "operator": "Electra",
  "status": "Operational",
  "num_connectors": 2,
  "connector_types": "CCS (Type 2)|Type 2 (Socket Only)",
  "date_added": "2025-11-02T09:58:00+00:00"
}
```

Analytics router (`/analytics`)

- `GET /analytics/count` — `{ "count": <int> }`.
- `GET /analytics/count_by_country` — grouped counts; query `limit` (default 50).
- `GET /analytics/nearest` — required query `lat`, `lon`; optional `radius_km` (10.0) and `limit` (10).
  - Returns list of `{ "distance_km": float, "station": { ... } }`.
  - Computation: Haversine distance in Python (no spatial index).
- `GET /analytics/by_operator` — query `operator` (string), returns list of stations.

Examples

```bash
curl 'http://127.0.0.1:8000/stations/?skip=0&limit=10'
curl 'http://127.0.0.1:8000/analytics/nearest?lat=50.68&lon=3.06&radius_km=5'
```

----

**Dataset (app/data/ev_stations_2025.csv)**

Columns

- `id` — integer
- `title`, `address`, `town`, `state`, `postcode`, `country`
- `lat`, `lon` — floats
- `operator`, `status`
- `num_connectors` — integer
- `connector_types` — pipe-separated list
- `date_added` — ISO datetime

Parsing notes (see `app/database.py`)

- `lat`/`lon` parsed with `float()`, malformed values become `NULL`.
- `num_connectors` parsed with `int()`, malformed values become `NULL`.
- `date_added` parsed with `datetime.fromisoformat()` after replacing `Z` with `+00:00`.

Storage

- SQLAlchemy model `EVStation` in `app/models.py` mirrors CSV fields.

----

**Testing & Notes**

Run tests:

```bash
pytest -q
```

- Tests are in `tests/test_api.py`. The test suite calls `init_db()` to ensure tables exist and sample data
  is loaded. Tests perform CRUD operations and call analytics endpoints.
- Tests run against the local SQLite DB and may modify it. To run tests against a temporary DB set `DATABASE_URL`
  to point to an ephemeral file before running `pytest`.

Example (use temp DB):

```bash
export DATABASE_URL="sqlite:///./test_ev_stations.db"
pytest -q
```

Notes for maintainers

- The codebase uses simple SQLAlchemy patterns compatible with SQLAlchemy 1.4; some warnings appear under
  SQLAlchemy 2.0 and Pydantic 2.x but they do not break tests. Consider upgrading models and Pydantic usage for
  future-proofing.

----

If you want, I can also remove the separate `API.md`, `SETUP.md`, `TESTING.md`, and `DATA.md` files or keep them
as backups; tell me which you prefer.
