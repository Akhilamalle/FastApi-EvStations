# Dataset description

The project includes a bundled CSV dataset at `app/data/ev_stations_2025.csv` which is imported into the
`ev_stations` database table on first startup.

CSV header (columns)

- `id` — integer primary id
- `title` — display title/name of the station
- `address` — street address
- `town` — town or city
- `state` — state or administrative region
- `postcode` — postal code
- `country` — ISO country code (e.g., `FR`)
- `lat` — latitude (float)
- `lon` — longitude (float)
- `operator` — charging network/operator name
- `status` — textual status (e.g., `Operational`)
- `num_connectors` — integer number of connectors
- `connector_types` — pipe-separated list of connector type descriptions
- `date_added` — ISO datetime (example: `2025-11-02 09:58:00+00:00`)

Parsing notes (see `app/database.py`)

- `lat`, `lon` are parsed with `float()` when present; malformed values become `NULL`.
- `num_connectors` is parsed with `int()` when present; malformed values become `NULL`.
- `date_added` is parsed using `datetime.fromisoformat()` after replacing `Z` with `+00:00`.

Storage (SQLAlchemy model)

The table schema is defined in `app/models.py` as `EVStation` with the same fields. Pydantic schemas in
`app/schemas.py` mirror these fields for input and output validation.

Data quality

- The CSV may contain incomplete or inconsistent records; the import logic is designed to be robust and
  tolerate issues by using `None` for problematic fields.
- For production use, consider pre-validating or normalizing data and using a spatial database/index for
  efficient geo queries.
