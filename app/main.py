from fastapi import FastAPI

from .database import init_db
from .routers import stations as stations_router
from .routers import analytics as analytics_router

app = FastAPI(title="EV Stations API")

app.include_router(stations_router.router)
app.include_router(analytics_router.router)


@app.on_event("startup")
def on_startup():
    # create tables and load sample CSV data if DB empty
    init_db()


@app.get("/healthz")
def health():
    return {"status": "ok"}
