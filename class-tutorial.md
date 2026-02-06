# Pytest with FastAPI - Class Tutorial
## Step-by-Step Guide for Teaching

---

## 🎯 **CLASS OBJECTIVE**
By the end of this class, students will:
- Set up a FastAPI project using UV
- Create a working API
- Write comprehensive tests using pytest
- Understand fixtures and test isolation

**Estimated Time:** 90 minutes

---

## 📋 **SETUP (5 minutes)**

### Step 1: Check Prerequisites
**Say to students:** "First, let's make sure everyone has Python installed."

**Command to run:**
```bash
python --version
```

**Expected:** Python 3.8 or higher

---

## 🚀 **PART 1: PROJECT SETUP (15 minutes)**

### Step 2: Install UV
**Say:** "We'll use UV, a fast Python package manager. Let's install it."

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Or using pip:**
```bash
pip install uv
```

**Verify:**
```bash
uv --version
```

---

### Step 3: Create Project Directory
**Say:** "Let's create a new folder for our project."

**Commands:**
```bash
mkdir fastapi-pytest-class
cd fastapi-pytest-class
```

---

### Step 4: Initialize UV Project
**Say:** "Now we'll initialize a new UV project. This creates the project structure."

**Command:**
```bash
uv init
```

**What this does:**
- Creates `pyproject.toml` (project configuration)
- Sets up Python version

**Show students the created files.**

---

### Step 5: Install Dependencies
**Say:** "We need FastAPI to build our API, and pytest to test it."

**Commands:**
```bash
uv add fastapi uvicorn[standard]
uv add --dev pytest pytest-asyncio httpx
```

**Explain each package:**
- `fastapi` - Web framework
- `uvicorn` - Server to run FastAPI
- `pytest` - Testing framework
- `httpx` - For testing HTTP requests

**Verify:**
```bash
uv pip list
```

---

## 🏗️ **PART 2: CREATE THE API (20 minutes)**

### Step 6: Create Project Structure
**Say:** "Let's organize our code properly."

**Create directories:**
```bash
mkdir app
mkdir tests
```

**Project structure should look like:**
```
fastapi-pytest-class/
├── app/
├── tests/
└── pyproject.toml
```

---

### Step 7: Create Empty Init Files
**Say:** "These files make Python treat directories as packages."

**Create `app/__init__.py`:**
```python
# Empty file - makes app a package
```

**Create `tests/__init__.py`:**
```python
# Empty file - makes tests a package
```

---

### Step 8: Create the FastAPI Application
**Say:** "Now let's build our Student Management API. I'll show you the code, then we'll type it together."

**Create `app/main.py` - Type this together:**

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Student Management API",
    description="A simple API to manage students",
    version="1.0.0"
)

# In-memory database
students_db = []
next_id = 1

# Data models
class Student(BaseModel):
    id: Optional[int] = None
    name: str
    age: int
    email: str
    course: str

class StudentCreate(BaseModel):
    name: str
    age: int
    email: str
    course: str

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None
    course: Optional[str] = None

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to Student Management API",
        "version": "1.0.0"
    }

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Get all students
@app.get("/students", response_model=List[Student])
def get_students():
    return students_db

# Get student by ID
@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    student = next((s for s in students_db if s["id"] == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# Create student
@app.post("/students", response_model=Student, status_code=201)
def create_student(student: StudentCreate):
    global next_id
    new_student = {
        "id": next_id,
        "name": student.name,
        "age": student.age,
        "email": student.email,
        "course": student.course
    }
    students_db.append(new_student)
    next_id += 1
    return new_student

# Update student
@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student_update: StudentUpdate):
    student = next((s for s in students_db if s["id"] == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    if student_update.name is not None:
        student["name"] = student_update.name
    if student_update.age is not None:
        student["age"] = student_update.age
    if student_update.email is not None:
        student["email"] = student_update.email
    if student_update.course is not None:
        student["course"] = student_update.course
    
    return student

# Delete student
@app.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: int):
    global students_db
    student = next((s for s in students_db if s["id"] == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    students_db = [s for s in students_db if s["id"] != student_id]
    return None
```

---

### Step 9: Test the API Manually
**Say:** "Let's start the server and see our API in action!"

**Start server:**
```bash
uvicorn app.main:app --reload
```

**Open browser:** `http://localhost:8000/docs`

**Show students:**
- Interactive API documentation
- Try creating a student
- Show the response

**Stop server:** Press `Ctrl+C`

---

## 🧪 **PART 3: INTRODUCTION TO PYTEST (10 minutes)**

### Step 10: What is Pytest?
**Say:** "Pytest is a testing framework. It makes writing tests simple."

**Key points:**
- Simple syntax (just use `assert`)
- Automatically finds tests
- Great error messages
- Powerful features (fixtures, parametrization)

**What is `assert`?**
**Say:** "`assert` is a Python keyword that checks if something is True. If it's True, the test passes. If it's False, the test fails."

**Examples:**
```python
assert 2 + 3 == 5        # ✅ Passes (True)
assert 2 + 3 == 6        # ❌ Fails (False)
assert "hello" == "hello"  # ✅ Passes (True)
assert 5 > 3             # ✅ Passes (True)
assert 1 > 10            # ❌ Fails (False)
```

**In pytest:**
- If `assert` is True → Test PASSES ✅
- If `assert` is False → Test FAILS ❌ (pytest shows you why)

---

### Step 11: Write Your First Test
**Say:** "Let's write a simple test to understand pytest."

**Create `tests/test_basics.py`:**

```python
def test_addition():
    """Test basic addition"""
    assert 2 + 3 == 5

def test_string_operations():
    """Test string operations"""
    name = "pytest"
    assert name.upper() == "PYTEST"
    assert "test" in name
```

**Run the test:**
```bash
pytest tests/test_basics.py -v
```

**Explain `assert` in detail:**
**Say:** "Let's break down what `assert` does:"

```python
assert 2 + 3 == 5
```

**What happens:**
1. Python evaluates: `2 + 3 == 5` → This is `True`
2. `assert True` → Test PASSES ✅
3. If it was `assert 2 + 3 == 6` → `False` → Test FAILS ❌

**Think of `assert` as saying:**
- "I assert that this should be True"
- "If it's not True, something is wrong!"

**Show students the output:**
- Green dots = passed
- Test names displayed
- Explain what `-v` (verbose) does

---

## 🔬 **PART 4: TESTING THE API (25 minutes)**

### Step 12: Set Up Test Client
**Say:** "To test FastAPI, we need a test client. Let's create our first API test."

**Create `tests/test_main.py`:**

```python
from fastapi.testclient import TestClient
from app.main import app

# Create test client
client = TestClient(app)
```

**Explain:** TestClient simulates HTTP requests without running a server.

---

### Step 13: Test Root Endpoint
**Say:** "Let's test our root endpoint."

**Add to `tests/test_main.py`:**

```python
def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to Student Management API",
        "version": "1.0.0"
    }
```

**Run test:**
```bash
pytest tests/test_main.py::test_read_root -v
```

**Show:** Green = test passed!

---

### Step 14: Test Health Check
**Say:** "Let's add another simple test."

**Add to `tests/test_main.py`:**

```python
def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
```

**Run:**
```bash
pytest tests/test_main.py -v
```

---

### Step 15: Test Creating a Student
**Say:** "Now let's test creating a student - this is more interesting!"

**Add to `tests/test_main.py`:**

```python
def test_create_student():
    """Test creating a new student"""
    student_data = {
        "name": "Alice Smith",
        "age": 22,
        "email": "alice@example.com",
        "course": "Mathematics"
    }
    response = client.post("/students", json=student_data)
    
    # Check status code
    assert response.status_code == 201
    
    # Check response data
    data = response.json()
    assert data["name"] == student_data["name"]
    assert data["age"] == student_data["age"]
    assert data["email"] == student_data["email"]
    assert data["course"] == student_data["course"]
    assert data["id"] is not None
```

**Run:**
```bash
pytest tests/test_main.py::test_create_student -v
```

**Explain:**
- Status code 201 = Created
- We check all fields
- ID is automatically assigned

---

### Step 16: The Problem - Test Isolation
**Say:** "Let's run all tests together and see what happens."

**Add another test:**

```python
def test_get_students():
    """Test getting all students"""
    response = client.get("/students")
    assert response.status_code == 200
    students = response.json()
    assert isinstance(students, list)
```

**Run all tests:**
```bash
pytest tests/test_main.py -v
```

**Problem:** Tests are affecting each other! The database persists between tests.

**Explain:** This is why we need fixtures.

---

## 🔧 **PART 5: FIXTURES - TEST ISOLATION (15 minutes)**

### Step 17: Understanding Fixtures
**Say:** "Fixtures help us set up and clean up before/after each test."

**Key concepts:**
- Setup code that runs before tests
- Teardown code that runs after tests
- Can be shared across tests
- `autouse=True` runs automatically

---

### Step 18: Create Fixtures
**Say:** "Let's add fixtures to reset our database before each test."

**Update `tests/test_main.py` - Add at the top:**

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app, students_db

@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_database():
    """Automatically reset database before each test"""
    students_db.clear()
    import app.main
    app.main.next_id = 1
    yield
    students_db.clear()
```

**Explain:**
- `client` fixture creates a fresh test client
- `reset_database` with `autouse=True` runs automatically
- `yield` separates setup from teardown
- Database is cleared before AND after each test

---

### Step 19: Update Tests to Use Fixtures
**Say:** "Now we need to update our tests to use the client fixture."

**Update all test functions to accept `client` parameter:**

```python
def test_read_root(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to Student Management API",
        "version": "1.0.0"
    }

def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_student(client):
    """Test creating a new student"""
    student_data = {
        "name": "Alice Smith",
        "age": 22,
        "email": "alice@example.com",
        "course": "Mathematics"
    }
    response = client.post("/students", json=student_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == student_data["name"]
    assert data["age"] == student_data["age"]
    assert data["email"] == student_data["email"]
    assert data["course"] == student_data["course"]
    assert data["id"] == 1  # First student should have ID 1

def test_get_students_empty(client):
    """Test getting all students when empty"""
    response = client.get("/students")
    assert response.status_code == 200
    students = response.json()
    assert isinstance(students, list)
    assert len(students) == 0
```

**Run all tests:**
```bash
pytest tests/test_main.py -v
```

**Success!** All tests pass and are independent.

---

## 📝 **PART 6: COMPLETE CRUD TESTS (15 minutes)**

### Step 20: Test Get Student by ID
**Say:** "Let's add tests for getting a specific student."

**Add to `tests/test_main.py`:**

```python
def test_get_student_by_id(client):
    """Test getting a specific student by ID"""
    # Create a student first
    student_data = {
        "name": "Charlie Brown",
        "age": 23,
        "email": "charlie@example.com",
        "course": "Chemistry"
    }
    create_response = client.post("/students", json=student_data)
    student_id = create_response.json()["id"]
    
    # Get the student by ID
    response = client.get(f"/students/{student_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == student_id
    assert data["name"] == student_data["name"]

def test_get_student_not_found(client):
    """Test getting a student that doesn't exist"""
    response = client.get("/students/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
```

**Explain:** We test both success (200) and failure (404) cases.

---

### Step 21: Test Update Student
**Say:** "Let's test updating a student."

**Add to `tests/test_main.py`:**

```python
def test_update_student(client):
    """Test updating a student"""
    # Create a student first
    student_data = {
        "name": "David Wilson",
        "age": 24,
        "email": "david@example.com",
        "course": "Biology"
    }
    create_response = client.post("/students", json=student_data)
    student_id = create_response.json()["id"]
    
    # Update the student
    update_data = {
        "name": "David Wilson Jr.",
        "age": 25
    }
    response = client.put(f"/students/{student_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "David Wilson Jr."
    assert data["age"] == 25
    assert data["email"] == student_data["email"]  # Unchanged
```

---

### Step 22: Test Delete Student
**Say:** "Finally, let's test deleting a student."

**Add to `tests/test_main.py`:**

```python
def test_delete_student(client):
    """Test deleting a student"""
    # Create a student first
    student_data = {
        "name": "Eve Davis",
        "age": 20,
        "email": "eve@example.com",
        "course": "History"
    }
    create_response = client.post("/students", json=student_data)
    student_id = create_response.json()["id"]
    
    # Delete the student
    response = client.delete(f"/students/{student_id}")
    assert response.status_code == 204
    
    # Verify student is deleted
    get_response = client.get(f"/students/{student_id}")
    assert get_response.status_code == 404
```

---

### Step 23: Run All Tests
**Say:** "Let's run all our tests and see everything pass!"

**Command:**
```bash
pytest tests/test_main.py -v
```

**Show students:**
- All tests passing
- Test count
- Time taken

---

## 🎓 **PART 7: ADVANCED - PARAMETRIZATION (10 minutes)**

### Step 24: Introduction to Parametrization
**Say:** "Instead of writing multiple similar tests, we can use parametrization."

**Add to `tests/test_main.py`:**

```python
@pytest.mark.parametrize("name,age,email,course", [
    ("Student One", 20, "one@example.com", "Math"),
    ("Student Two", 21, "two@example.com", "Science"),
    ("Student Three", 22, "three@example.com", "English"),
])
def test_create_multiple_students(client, name, age, email, course):
    """Test creating multiple students with different data"""
    student_data = {
        "name": name,
        "age": age,
        "email": email,
        "course": course
    }
    response = client.post("/students", json=student_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == name
    assert data["age"] == age
    assert data["email"] == email
    assert data["course"] == course
```

**Run:**
```bash
pytest tests/test_main.py::test_create_multiple_students -v
```

**Show:** One test function runs 3 times with different data!

---

## 📊 **PART 8: TEST COVERAGE (5 minutes)**

### Step 25: Check Test Coverage
**Say:** "Let's see how much of our code is tested."

**Install coverage:**
```bash
uv add --dev pytest-cov
```

**Run with coverage:**
```bash
pytest --cov=app --cov-report=term-missing
```

**Explain the output:**
- Percentage covered
- Which lines are missing
- Goal: 80%+ coverage

---

## ✅ **WRAP-UP (5 minutes)**

### Step 26: Summary
**Review what we learned:**

1. ✅ Set up project with UV
2. ✅ Created FastAPI application
3. ✅ Wrote pytest tests
4. ✅ Used fixtures for test isolation
5. ✅ Tested all CRUD operations
6. ✅ Used parametrization

### Key Takeaways:
- **Tests should be independent** - Use fixtures!
- **Test both success and failure** - Happy path + error cases
- **Clear test names** - `test_<what>_<condition>_<expected>`
- **Coverage matters** - Know what's tested

---

## 🎯 **QUICK REFERENCE**

### Common Pytest Commands:
```bash
pytest                    # Run all tests
pytest -v                 # Verbose output
pytest -k "create"        # Run tests matching pattern
pytest -x                 # Stop on first failure
pytest --cov=app          # Run with coverage
```

### Test Structure:
```python
def test_something(client):
    # Arrange: Set up data
    data = {...}
    
    # Act: Perform action
    response = client.post("/endpoint", json=data)
    
    # Assert: Check result
    assert response.status_code == 201
```

---

## 📚 **HOMEWORK/PRACTICE**

### Exercise 1: Add More Tests
- Test update with invalid ID
- Test delete with invalid ID
- Test creating student with missing fields

### Exercise 2: Add Validation
- Add email format validation
- Add age must be positive
- Write tests for these validations

### Exercise 3: Add Search Endpoint
- Create `/students/search?course=Math` endpoint
- Write tests for it

---

## ❓ **COMMON QUESTIONS**

**Q: Why do we need fixtures?**
A: To ensure tests don't affect each other. Each test should start with a clean state.

**Q: What does `autouse=True` do?**
A: Makes the fixture run automatically for every test, without needing to pass it as a parameter.

**Q: Can I skip tests?**
A: Yes! Use `@pytest.mark.skip` or `@pytest.mark.skipif`

**Q: How do I test async endpoints?**
A: Use `httpx.AsyncClient` and `@pytest.mark.asyncio`

---

## 🎉 **END OF CLASS**

**Congratulations!** You now know how to:
- Set up a FastAPI project
- Write comprehensive tests with pytest
- Use fixtures for test isolation
- Test API endpoints properly

**Next Steps:**
- Practice writing more tests
- Explore pytest plugins
- Learn about mocking external services
- Try Test-Driven Development (TDD)

---

**Happy Testing! 🚀**
