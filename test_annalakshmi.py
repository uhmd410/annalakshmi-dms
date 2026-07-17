import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

TEST_DB_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

SAMPLE = {
    "full_name": "Test User",
    "mobile_number": "9876543210",
    "email": "test.user@example.com",
    "address": "123 Test Street",
    "area": "Test Area",
    "city": "Bangalore",
    "state": "Karnataka",
    "pin_code": "560001",
    "cuisine_specialization": "South Indian",
    "veg_or_nonveg": "veg",
    "signature_dishes": "Dosa",
    "available_timings": "8 AM - 12 PM",
    "max_orders_per_day": 10,
    "date_joined": "2026-01-01",
    "status": "active",
}


def test_create_record():
    res = client.post("/annalakshmis/", json=SAMPLE)
    assert res.status_code == 200
    data = res.json()
    assert data["full_name"] == "Test User"
    assert "created_at" in data and "updated_at" in data


def test_create_duplicate_mobile_fails():
    client.post("/annalakshmis/", json=SAMPLE)
    res = client.post("/annalakshmis/", json=SAMPLE)
    assert res.status_code == 400
    assert res.json()["error"] is True


def test_create_invalid_email_fails():
    res = client.post("/annalakshmis/", json={**SAMPLE, "email": "not-an-email"})
    assert res.status_code == 422


def test_create_invalid_mobile_fails():
    res = client.post("/annalakshmis/", json={**SAMPLE, "mobile_number": "12345"})
    assert res.status_code == 422


def test_create_invalid_pin_fails():
    res = client.post("/annalakshmis/", json={**SAMPLE, "pin_code": "12A45"})
    assert res.status_code == 422


def test_get_by_id():
    created = client.post("/annalakshmis/", json=SAMPLE).json()
    res = client.get(f"/annalakshmis/{created['id']}")
    assert res.status_code == 200


def test_get_by_id_not_found():
    res = client.get("/annalakshmis/9999")
    assert res.status_code == 404


def test_update_record():
    created = client.post("/annalakshmis/", json=SAMPLE).json()
    res = client.put(f"/annalakshmis/{created['id']}", json={"area": "New Area"})
    assert res.status_code == 200
    assert res.json()["area"] == "New Area"


def test_archive_is_idempotent():
    created = client.post("/annalakshmis/", json=SAMPLE).json()
    assert client.patch(f"/annalakshmis/{created['id']}/archive").json()["status"] == "inactive"
    res2 = client.patch(f"/annalakshmis/{created['id']}/archive")
    assert res2.status_code == 200


def test_pagination():
    for i in range(15):
        client.post("/annalakshmis/", json={**SAMPLE, "mobile_number": f"90000000{i:02d}"})
    res = client.get("/annalakshmis/?page=1&page_size=10")
    data = res.json()
    assert data["total"] == 15
    assert len(data["items"]) == 10
    assert data["total_pages"] == 2


def test_filter_by_status():
    created = client.post("/annalakshmis/", json=SAMPLE).json()
    client.patch(f"/annalakshmis/{created['id']}/archive")
    res = client.get("/annalakshmis/?status=inactive")
    assert all(item["status"] == "inactive" for item in res.json()["items"])


def test_dashboard_summary():
    client.post("/annalakshmis/", json=SAMPLE)
    res = client.get("/dashboard/summary")
    data = res.json()
    assert "total" in data and "active" in data and "inactive" in data