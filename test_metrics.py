from collections import namedtuple
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db

# Setup in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def run_around_tests():
    # Clean up before each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

def test_metrics_country():
    # Setup some dummy data
    client.post("/employees/", json={"full_name": "A", "job_title": "Dev", "country": "India", "gross_salary": 50000.0})
    client.post("/employees/", json={"full_name": "B", "job_title": "Dev", "country": "India", "gross_salary": 150000.0})
    client.post("/employees/", json={"full_name": "C", "job_title": "Manager", "country": "India", "gross_salary": 100000.0})
    
    response = client.get("/metrics/country/India")
    assert response.status_code == 200
    data = response.json()
    assert data["country"] == "India"
    assert data["min_salary"] == 50000.0
    assert data["max_salary"] == 150000.0
    assert data["avg_salary"] == 100000.0

def test_metrics_country_not_found():
    response = client.get("/metrics/country/Nowhere")
    assert response.status_code == 404

def test_metrics_job_title():
    # Setup some dummy data
    client.post("/employees/", json={"full_name": "A", "job_title": "Dev", "country": "India", "gross_salary": 50000.0})
    client.post("/employees/", json={"full_name": "B", "job_title": "Dev", "country": "US", "gross_salary": 150000.0})
    client.post("/employees/", json={"full_name": "C", "job_title": "Dev", "country": "UK", "gross_salary": 100000.0})
    
    response = client.get("/metrics/job-title/Dev")
    assert response.status_code == 200
    data = response.json()
    assert data["job_title"] == "Dev"
    assert data["avg_salary"] == 100000.0

def test_metrics_job_title_not_found():
    response = client.get("/metrics/job-title/Astronaut")
    assert response.status_code == 404
