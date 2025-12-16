# Setup & Usage

This document explains how to set up and run the EV Stations FastAPI app locally.

Requirements

- Python 3.9+ (3.10/3.11 recommended)
- dependencies listed in `requirements.txt` (FastAPI, uvicorn, SQLAlchemy, pydantic, pytest...)

Installation (recommended)

1. Create a virtual environment and activate it:

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

Running the application

```bash
uvicorn app.main:app --reload
```

The server will start on `http://127.0.0.1:8000` by default. Visit `/docs` for interactive API docs.

Database and dataset

- By default the app uses SQLite and the URL `sqlite:///./ev_stations.db`.
- On startup the app will call `init_db()` (see `app/database.py`) which creates tables and will load
  `app/data/ev_stations_2025.csv` into the `ev_stations` table if the table is empty.
- To use a different database, set the `DATABASE_URL` environment variable before running the app, e.g.: 

```bash
export DATABASE_URL="postgresql+psycopg2://user:pass@host:5432/dbname"
# Windows (PowerShell)
$env:DATABASE_URL = 'postgresql+psycopg2://user:pass@host:5432/dbname'
```

Using Docker (optional)

There is no official Dockerfile in this repo; a minimal Dockerfile can be created that:

- installs Python dependencies
- exposes port 8000
- runs `uvicorn app.main:app --host 0.0.0.0`

Notes and tips

- CSV loading is basic: numeric and datetime parsing is tolerant but may drop malformed values.
- The `nearest` analytics endpoint performs in-Python distance computation and is not suitable for very
  large datasets — consider PostGIS or a spatial index for production.
