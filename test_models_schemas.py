from schemas import EmployeeCreate, EmployeeUpdate
from models import Employee
import pytest

def test_employee_create_schema_valid():
    emp = EmployeeCreate(
        full_name="John Doe",
        job_title="Software Engineer",
        country="India",
        gross_salary=100000.0
    )
    assert emp.full_name == "John Doe"
    assert emp.gross_salary == 100000.0

def test_employee_model_instantiation():
    emp = Employee(
        full_name="Jane Doe",
        job_title="Manager",
        country="United States",
        gross_salary=150000.0
    )
    assert emp.full_name == "Jane Doe"
    assert emp.country == "United States"
