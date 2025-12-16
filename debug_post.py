from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db

init_db()
client = TestClient(app)
payload = {"title": "Test Station", "town": "Testtown", "country": "TS", "lat": 10.0, "lon": 20.0}
r = client.post('/stations/', json=payload)
print('status', r.status_code)
try:
    print(r.json())
except Exception as e:
    print('no json', e)
