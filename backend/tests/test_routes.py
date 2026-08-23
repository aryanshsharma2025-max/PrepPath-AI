import io
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.opportunity_db import MOCK_OPPORTUNITIES_DB
from app.schemas.opportunity import OpportunityExtraction, RequirementExtraction, DocumentExtraction

client = TestClient(app)

def test_health_check():
    """Verify health check endpoint returns 200 and correct payload."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "PrepPath" in data["service"]

def test_root_endpoint():
    """Verify root endpoint provides API navigation info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["docs"] == "/docs"

def test_get_student_profile():
    """Verify profile GET returns student profile structure."""
    response = client.get("/api/profile")
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert data["user_id"] == "test-student-123"

def test_update_student_profile():
    """Verify profile POST correctly updates fields."""
    update_data = {
        "age": 20,
        "state": "Chhattisgarh",
        "family_income": 250000.0,
        "academic_percentage": 88.5,
        "course_level": "Undergraduate",
        "bpl_status": False,
        "attendance_percentage": 85.0
    }
    response = client.post("/api/profile", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["age"] == 20
    assert data["state"] == "Chhattisgarh"
    assert data["academic_percentage"] == 88.5

def test_analyze_opportunity_invalid_extension():
    """Verify upload rejects non-PDF file types with 400."""
    fake_file = io.BytesIO(b"Hello world")
    response = client.post(
        "/api/opportunities/analyze",
        files={"file": ("test.txt", fake_file, "text/plain")}
    )
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert "PDF documents" in data["error"]

def test_analyze_opportunity_corrupt_pdf():
    """Verify upload rejects invalid/empty PDF bytes with 400."""
    fake_pdf = io.BytesIO(b"Not a real pdf content")
    response = client.post(
        "/api/opportunities/analyze",
        files={"file": ("corrupt.pdf", fake_pdf, "application/pdf")}
    )
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False

def test_evaluate_eligibility_not_found():
    """Verify eligibility check for non-existent opportunity returns 404."""
    response = client.post("/api/opportunities/non-existent-id-9999/eligibility")
    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert "not found" in data["error"]

def test_evaluate_eligibility_success_with_stored_opportunity():
    """Verify deterministic eligibility check runs successfully against stored opportunity."""
    test_opp_id = "test-opp-001"
    MOCK_OPPORTUNITIES_DB[test_opp_id] = OpportunityExtraction(
        title="Test Merit Scholarship",
        provider="Dept of Higher Education",
        category="Scholarship",
        description="Merit based scholarship for undergraduate students",
        eligibility=[
            RequirementExtraction(
                requirement_type="academic",
                field="academic_percentage",
                operator=">=",
                value="75.0",
                unit="%"
            ),
            RequirementExtraction(
                requirement_type="financial",
                field="family_income",
                operator="<=",
                value="500000",
                unit="INR"
            )
        ],
        documents=[
            DocumentExtraction(
                document_type="income_certificate",
                name="Income Certificate",
                mandatory=True
            )
        ]
    )

    # Update profile to qualify
    client.post("/api/profile", json={
        "academic_percentage": 85.0,
        "family_income": 300000.0
    })

    response = client.post(f"/api/opportunities/{test_opp_id}/eligibility")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ELIGIBLE"
    assert len(data["passed"]) == 2
    assert len(data["failed"]) == 0
