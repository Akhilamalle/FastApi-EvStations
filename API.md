# API Reference

This document describes the HTTP API exposed by the FastAPI EV Stations service.

Base URL (local): http://127.0.0.1:8000

All endpoints also have OpenAPI docs at `/docs` (Swagger UI) when the server is running.

## Health

- GET `/healthz`
  - Response: 200
  - Body: `{ "status": "ok" }`

## Stations router

Prefix: `/stations`

- GET `/stations/`
  - Query parameters:
    - `skip` (int, default 0)
    - `limit` (int, default 100)
  - Response: 200
  - Body: JSON array of station objects (see schema below)

- GET `/stations/{id}`
  - Path parameter: `id` (int)
  - Response: 200 with station JSON, or 404 if not found

- POST `/stations/`
  - Body: JSON matching `EVStationCreate` (partial fields allowed)
  - Response: 201 with created station JSON

- PUT `/stations/{id}`
  - Body: JSON matching `EVStationUpdate` (partial fields allowed)
  - Response: 200 with updated station JSON, or 404 if not found

- DELETE `/stations/{id}`
  - Response: 204 on success, or 404 if not found

Station JSON schema (Pydantic `EVStationOut` / SQLAlchemy `EVStation`):

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

## Analytics router

Prefix: `/analytics`

- GET `/analytics/count`
  - Response: 200
  - Body: `{ "count": <int> }`

- GET `/analytics/count_by_country`
  - Query params: `limit` (int, default 50)
  - Response: 200
  - Body: list of `{ "country": "XX", "count": n }` ordered by count desc

- GET `/analytics/nearest`
  - Query params (required): `lat` (float), `lon` (float)
  - Optional: `radius_km` (float, default 10.0), `limit` (int, default 10)
  - Response: 200
  - Body: list of `{ "distance_km": float, "station": { ... } }`
  - Notes: Uses a simple Haversine calculation in Python; not spatially indexed.

- GET `/analytics/by_operator`
  - Query param: `operator` (string)
  - Response: 200
  - Body: list of station objects for that operator

## Examples

List stations (first 10):

```bash
curl 'http://127.0.0.1:8000/stations/?skip=0&limit=10'
```

Find nearest stations:

```bash
curl 'http://127.0.0.1:8000/analytics/nearest?lat=50.68&lon=3.06&radius_km=5'
```
