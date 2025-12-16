# Testing

This project uses `pytest` and FastAPI's `TestClient` for tests located in the `tests/` folder.

Run tests

```bash
pytest -q
```

What the tests do

- `tests/test_api.py` boots the app and calls `init_db()` to ensure DB tables exist and sample data is loaded.
- Tests cover:
  - health endpoint
  - reading stations list
  - basic CRUD flow for a station (create, read, update, delete)
  - a few analytics endpoints

Notes

- Tests run against the local SQLite DB created by `init_db()`; they may modify the DB state (tests create and
  delete a station). If you want a clean DB for each test run, run tests in a temporary database by setting
  the `DATABASE_URL` env var to an ephemeral SQLite file before running tests.

Example (use temp DB):

```bash
export DATABASE_URL="sqlite:///./test_ev_stations.db"
pytest -q
```
