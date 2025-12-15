# EV Stations FastAPI

This project exposes a FastAPI service around an EV charging stations dataset (CSV).

Quick start

- Install dependencies:

```bash
python -m pip install -r requirements.txt
```

- Run locally:

```bash
uvicorn app.main:app --reload
```

The application will auto-create `ev_stations.db` and load the bundled CSV at startup.

API endpoints

- `GET /healthz` - health check
- `GET /stations/` - list stations (params: skip, limit)
- `GET /stations/{id}` - get station
- `POST /stations/` - create station (JSON)
- `PUT /stations/{id}` - update station (JSON)
- `DELETE /stations/{id}` - delete station
- `GET /analytics/count` - total count
- `GET /analytics/count_by_country` - counts grouped by country
- `GET /analytics/nearest?lat=&lon=&radius_km=&limit=` - nearest stations

Testing

```bash
pytest
```

CI/CD

- CI workflow is at `.github/workflows/ci.yml` - installs deps, runs tests, builds wheels.
- CD workflow for Azure Functions is at `.github/workflows/azure_deploy.yml`. Set the following GitHub secrets before push:
  - `AZURE_FUNCTIONAPP_NAME` - target function app name
  - `AZURE_CREDENTIALS` - JSON credentials created from Azure service principal

Azure deployment notes

1. Create an Azure Function App (Python) in your subscription.
2. Create a service principal and add to GitHub secrets `AZURE_CREDENTIALS` per Azure docs.
3. Push to `main` to trigger the deploy workflow.
