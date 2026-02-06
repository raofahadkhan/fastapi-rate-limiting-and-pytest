from fastapi.testclient import TestClient
from app.main import app

# Create test client
client = TestClient(app)

def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to Student Management API",
        "version": "1.0.0"
    }


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