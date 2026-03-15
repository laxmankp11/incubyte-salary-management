# Incubyte Salary Management API

This repository contains the solution for the Incubyte Salary Management Kata.
The system is implemented as a REST API that handles Employee records, gross/net salary calculations through deduction rules, and aggregated salary metrics. 

There is no UI, this is strictly a backend service.

## Tech Stack
- **Language**: Python 3.10+
- **Framework**: FastAPI
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Testing**: Pytest & HTTPX

## Core Features
1. **Employee CRUD Endpoint**
   - Manage employee records including Full Name, Job Title, Country, and Gross Salary.
2. **Salary Calculation Endpoint**
   - Calculates Net Salary given an employee's ID.
   - Applies country-based TDS rules:
     - India: `10%` deduction
     - United States (US): `12%` deduction 
     - Others: `0%` deduction
3. **Salary Metrics Endpoint**
   - Aggregates metrics (Min, Max, Avg) by specific Country.
   - Aggregates metrics (Avg) by specific Job Title.

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd incubyte-salary-management
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**:
   ```bash
   uvicorn main:app --reload
   ```
   *The API will be accessible at http://127.0.0.1:8000. You can visit http://127.0.0.1:8000/docs for the automatic Swagger UI documentation.*

## Testing (Strict TDD)
This project was developed using a strict Test-Driven Development (TDD) approach. Missing tests were written first (Red phase), implementation code followed (Green phase), and refactoring occurred naturally before committing. 

To run the tests:
```bash
pytest -v
```
*Coverage spans CRUD operations, calculation edge-cases, scaling dummy data for metrics, and resource-not-found exceptions.*

## Implementation Details & AI Usage (Transparency)
As requested by the Kata requirements, here is the transparency layer regarding AI usage:
- **Assistant Used**: Google Deepmind's Advanced Agentic Assistant. 
- **Rationale**: Used heavily to scaffold the boilerplate FastAPI architecture, design coherent SQLAlchemy models, write granular Pytest tests strictly adhering to the TDD loop, and debug Pytest teardown scope issues. It provided speed while maintaining production-like project qualities.
- **Workflow**: 
  - Iterative `task.md` checklists and `implementation_plan.md` alignment before execution.
  - Test specifications were intentionally authored to fail with `404 Not Found` (since endpoints did not exist), followed immediately by the endpoint logic being injected via atomic `git commit` loops.
  - The prompt and methodology were documented locally to keep the AI focused on the kata requirements natively inside its workspace context.
