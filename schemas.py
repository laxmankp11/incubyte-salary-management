from pydantic import BaseModel
from typing import Optional

class EmployeeBase(BaseModel):
    full_name: str
    job_title: str
    country: str
    gross_salary: float

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    job_title: Optional[str] = None
    country: Optional[str] = None
    gross_salary: Optional[float] = None

class EmployeeResponse(EmployeeBase):
    id: int

    class Config:
        from_attributes = True

class SalaryResponse(BaseModel):
    id: int
    gross_salary: float
    deduction_percentage: str
    deduction_amount: float
    net_salary: float

class MetricsCountryResponse(BaseModel):
    country: str
    min_salary: float
    max_salary: float
    avg_salary: float

class MetricsJobTitleResponse(BaseModel):
    job_title: str
    avg_salary: float
