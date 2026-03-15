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

def test_create_employee():
    payload = {
        "full_name": "Laxman KP",
        "job_title": "Software Engineer",
        "country": "India",
        "gross_salary": 120000.0
    }
    response = client.post("/employees/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["full_name"] == "Laxman KP"
    assert data["gross_salary"] == 120000.0

def test_get_employee():
    payload = {
        "full_name": "John Doe",
        "job_title": "Manager",
        "country": "United States",
        "gross_salary": 150000.0
    }
    create_response = client.post("/employees/", json=payload)
    emp_id = create_response.json()["id"]

    response = client.get(f"/employees/{emp_id}")
    assert response.status_code == 200
    assert response.json()["full_name"] == "John Doe"

def test_get_employee_not_found():
    response = client.get("/employees/999")
    assert response.status_code == 404

def test_update_employee():
    payload = {
        "full_name": "Jane",
        "job_title": "Tester",
        "country": "UK",
        "gross_salary": 50000.0
    }
    create_response = client.post("/employees/", json=payload)
    emp_id = create_response.json()["id"]

    update_payload = {"full_name": "Jane Smith", "gross_salary": 60000.0}
    response = client.put(f"/employees/{emp_id}", json=update_payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Jane Smith"
    assert data["gross_salary"] == 60000.0
    assert data["country"] == "UK" # unaffected fields remain same

def test_delete_employee():
    payload = {
        "full_name": "To Be Deleted",
        "job_title": "Temp",
        "country": "Canada",
        "gross_salary": 45000.0
    }
    create_response = client.post("/employees/", json=payload)
    emp_id = create_response.json()["id"]

    delete_response = client.delete(f"/employees/{emp_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/employees/{emp_id}")
    assert get_response.status_code == 404

def test_salary_calculation_india():
    payload = {
        "full_name": "Ravi",
        "job_title": "Developer",
        "country": "India",
        "gross_salary": 100000.0
    }
    create_response = client.post("/employees/", json=payload)
    emp_id = create_response.json()["id"]

    response = client.get(f"/employees/{emp_id}/salary")
    assert response.status_code == 200
    data = response.json()
    assert data["gross_salary"] == 100000.0
    assert data["deduction_percentage"] == "10%"
    assert data["deduction_amount"] == 10000.0
    assert data["net_salary"] == 90000.0

def test_salary_calculation_usa():
    payload = {
        "full_name": "Bob",
        "job_title": "Developer",
        "country": "United States",
        "gross_salary": 100000.0
    }
    create_response = client.post("/employees/", json=payload)
    emp_id = create_response.json()["id"]

    response = client.get(f"/employees/{emp_id}/salary")
    assert response.status_code == 200
    data = response.json()
    assert data["deduction_percentage"] == "12%"
    assert data["deduction_amount"] == 12000.0
    assert data["net_salary"] == 88000.0

def test_salary_calculation_other_country():
    payload = {
        "full_name": "Pierre",
        "job_title": "Developer",
        "country": "France",
        "gross_salary": 100000.0
    }
    create_response = client.post("/employees/", json=payload)
    emp_id = create_response.json()["id"]

    response = client.get(f"/employees/{emp_id}/salary")
    assert response.status_code == 200
    data = response.json()
    assert data["deduction_percentage"] == "0%"
    assert data["deduction_amount"] == 0.0
    assert data["net_salary"] == 100000.0
