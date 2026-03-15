from sqlalchemy import Column, Integer, String, Float
from database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    job_title = Column(String, index=True)
    country = Column(String, index=True)
    gross_salary = Column(Float)
