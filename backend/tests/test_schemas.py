import pytest
from app.schemas.opportunity import (
    OpportunityExtraction,
    RequirementExtraction,
    DocumentExtraction,
)


def test_opportunity_schema_valid():
    """Test validating a complete valid OpportunityExtraction instance."""
    data = {
        "title": "National Higher Education Scholarship",
        "provider": "Department of Higher Education",
        "category": "Scholarship",
        "benefit": "INR 50,000 per annum",
        "deadline": "2026-10-31",
        "official_url": "https://scholarships.gov.in",
        "eligibility": [
            {
                "requirement_type": "academic",
                "field": "minimum_percentage",
                "operator": ">=",
                "value": "75",
                "unit": "%",
                "mandatory": True,
                "description": "Must have scored 75% or above in 12th Board Exams",
                "source_text": "Applicants must secure at least 75% marks in Class 12."
            }
        ],
        "documents": [
            {
                "document_type": "income_certificate",
                "name": "Family Income Certificate",
                "mandatory": True,
                "description": "Issued by competent revenue authority",
                "source_text": "Valid Income Certificate is compulsory."
            }
        ]
    }

    opportunity = OpportunityExtraction.model_validate(data)
    assert opportunity.title == "National Higher Education Scholarship"
    assert opportunity.provider == "Department of Higher Education"
    assert len(opportunity.eligibility) == 1
    assert opportunity.eligibility[0].field == "minimum_percentage"
    assert opportunity.eligibility[0].value == "75"
    assert len(opportunity.documents) == 1
    assert opportunity.documents[0].name == "Family Income Certificate"


def test_opportunity_schema_defaults():
    """Test opportunity schema with optional fields omitted."""
    data = {
        "title": "Minimal Merit Grant"
    }

    opportunity = OpportunityExtraction.model_validate(data)
    assert opportunity.title == "Minimal Merit Grant"
    assert opportunity.provider is None
    assert opportunity.category == "Scholarship"
    assert opportunity.eligibility == []
    assert opportunity.documents == []
