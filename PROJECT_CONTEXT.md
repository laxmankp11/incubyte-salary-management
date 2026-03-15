# Project Context: Incubyte Salary Management API

## Objective
Implement the Incubyte Salary Management Kata as an API using Test-Driven Development (TDD). The objective is to build a high-quality, production-ready REST API that handles a basic Employee CRUD and endpoints for salary calculation and metrics aggregation.

## Requirements Overview
1. **API Application**: Has no UI, only an API surface.
2. **Employee Profile Requirements**:
   - `full_name` (string)
   - `job_title` (string)
   - `country` (string)
   - `salary` (float/gross)
3. **Database**: Must use SQLite to store records.
4. **Endpoint 1: Employee CRUD**
   - Create, Read, Update, Delete for the Employee resource.
5. **Endpoint 2: Salary Calculation**
   - Given an Employee ID, calculate the net salary from gross salary.
   - **India**: 10% deduction of gross (Net = 90% Gross)
   - **United States**: 12% deduction of gross (Net = 88% Gross)
   - **Other Countries**: 0% deductions (Net = 100% Gross)
6. **Endpoint 3: Salary Metrics**
   - Country-based: Minimum, maximum, and average salary for a given country.
   - Job Title-based: Average salary for all employees with a specific job title.

## Technical Details and Dependencies
- **Programming Language**: Python
- **Framework**: FastAPI (for automatic interactive API documentation, rapid development, and high performance)
- **Database ORM**: SQLAlchemy 
- **Database Engine**: SQLite
- **Dependency Management**: Standard `requirements.txt`
- **Testing**: `pytest` and `httpx` (strictly TDD workflow)

## Approach: Test-Driven Development (TDD)
- For every feature (Employee CRUD, Salary Calculation, Salary Metrics), we will first write failing tests (`Red`).
- We will implement the minimal code required to pass the test (`Green`).
- Finally, we refine and clean up the logic (`Refactor`).
- Regular atomic commits will be made at each step to demonstrate the code evolution.

## AI Usage & Implementation Remarks
We have leveraged AI (Google Deepmind Assistant) to scaffold the FastAPI structural logic, generate comprehensive test cases based on Kata requirements, and strictly drive the TDD workflow. Appropriate `chore:`, `test:`, `feat:`, and `refactor:` git annotations are used to show AI-driven intentionality for each cycle.

*Note: This doc provides context for later ingestion, ensuring we have a quick-reference for the Kata's boundaries and initial design.*
