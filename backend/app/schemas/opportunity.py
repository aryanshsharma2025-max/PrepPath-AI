"""
Pydantic Schemas for Opportunity Analysis and Structured AI Output.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class RequirementExtraction(BaseModel):
    requirement_type: str = Field(
        ...,
        description="Type of requirement e.g. 'academic', 'income', 'age', 'gender', 'degree', 'caste_category', 'other'"
    )
    field: str = Field(
        ...,
        description="Specific field identifier e.g. 'minimum_percentage', 'family_income', 'course', 'age_limit'"
    )
    operator: Optional[str] = Field(
        None,
        description="Comparison operator if applicable e.g. '>=', '<=', '=', 'in'"
    )
    value: Optional[str] = Field(
        None,
        description="Value requirement e.g. '75', '800000', 'Undergraduate'"
    )
    unit: Optional[str] = Field(
        None,
        description="Unit e.g. '%', 'INR', 'years'"
    )
    mandatory: bool = Field(
        True,
        description="Whether this criterion is mandatory for eligibility"
    )
    description: Optional[str] = Field(
        None,
        description="Human-readable description of the requirement"
    )
    source_text: Optional[str] = Field(
        None,
        description="Exact quote or snippet from original document supporting this requirement"
    )


class DocumentExtraction(BaseModel):
    document_type: str = Field(
        ...,
        description="Document category e.g. 'income_certificate', 'marksheet', 'id_proof', 'caste_certificate', 'other'"
    )
    name: str = Field(
        ...,
        description="Display name of the document e.g. 'Income Certificate', 'Class 10/12 Marksheet'"
    )
    mandatory: bool = Field(
        True,
        description="Whether this document is mandatory for application submission"
    )
    description: Optional[str] = Field(
        None,
        description="Document details or instructions"
    )
    source_text: Optional[str] = Field(
        None,
        description="Exact snippet from original document mentioning this required document"
    )


class OpportunityExtraction(BaseModel):
    title: str = Field(
        ...,
        description="Title of the scholarship or opportunity"
    )
    provider: Optional[str] = Field(
        None,
        description="Organization, government agency, or institution offering the opportunity"
    )
    category: str = Field(
        "Scholarship",
        description="Category e.g. 'Scholarship', 'Fellowship', 'Grant'"
    )
    description: Optional[str] = Field(
        None,
        description="High-level overview of the opportunity"
    )
    benefit: Optional[str] = Field(
        None,
        description="Financial award, tuition coverage, allowance, or benefits provided"
    )
    deadline: Optional[str] = Field(
        None,
        description="Application deadline date (YYYY-MM-DD or textual date if unclear)"
    )
    official_url: Optional[str] = Field(
        None,
        description="Official portal or application website URL"
    )
    eligibility: List[RequirementExtraction] = Field(
        default_factory=list,
        description="Structured list of eligibility requirements"
    )
    documents: List[DocumentExtraction] = Field(
        default_factory=list,
        description="Structured list of required application documents"
    )


class OpportunityResponse(BaseModel):
    success: bool
    opportunity: Optional[OpportunityExtraction] = None
    error: Optional[str] = None
