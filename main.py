from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import engine, get_db, Base
import models
import schemas

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Incubyte Salary Management API")

@app.post("/employees/", response_model=schemas.EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = models.Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.get("/employees/", response_model=List[schemas.EmployeeResponse])
def get_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    employees = db.query(models.Employee).offset(skip).limit(limit).all()
    return employees

@app.get("/employees/{employee_id}", response_model=schemas.EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.put("/employees/{employee_id}", response_model=schemas.EmployeeResponse)
def update_employee(employee_id: int, employee_update: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    update_data = employee_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_employee, key, value)
        
    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(db_employee)
    db.commit()
    return None

@app.get("/employees/{employee_id}/salary", response_model=schemas.SalaryResponse)
def calculate_salary(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    country = employee.country.lower()
    gross = employee.gross_salary
    
    if country == "india":
        deduction_pct = 10
    elif country == "united states" or country == "us" or country == "usa":
        deduction_pct = 12
    else:
        # Default for other countries
        deduction_pct = 0
        
    deduction_amount = (gross * deduction_pct) / 100.0
    net_salary = gross - deduction_amount
    
    return schemas.SalaryResponse(
        id=employee.id,
        gross_salary=gross,
        deduction_percentage=f"{deduction_pct}%",
        deduction_amount=deduction_amount,
        net_salary=net_salary
    )

from sqlalchemy.sql import func

@app.get("/metrics/country/{country}", response_model=schemas.MetricsCountryResponse)
def get_metrics_by_country(country: str, db: Session = Depends(get_db)):
    result = db.query(
        func.min(models.Employee.gross_salary).label("min_salary"),
        func.max(models.Employee.gross_salary).label("max_salary"),
        func.avg(models.Employee.gross_salary).label("avg_salary")
    ).filter(
        func.lower(models.Employee.country) == country.lower()
    ).first()

    if not result or result.min_salary is None:
        raise HTTPException(status_code=404, detail="No employees found for this country")

    return schemas.MetricsCountryResponse(
        country=country.title() if country.lower() != "us" and country.lower() != "usa" and country.lower() != "uk" else country.upper(),
        min_salary=result.min_salary,
        max_salary=result.max_salary,
        avg_salary=result.avg_salary
    )

@app.get("/metrics/job-title/{job_title}", response_model=schemas.MetricsJobTitleResponse)
def get_metrics_by_job_title(job_title: str, db: Session = Depends(get_db)):
    result = db.query(
        func.avg(models.Employee.gross_salary).label("avg_salary")
    ).filter(
        func.lower(models.Employee.job_title) == job_title.lower()
    ).first()

    if not result or result.avg_salary is None:
        raise HTTPException(status_code=404, detail="No employees found for this job title")

    return schemas.MetricsJobTitleResponse(
        job_title=job_title.title(),
        avg_salary=result.avg_salary
    )
