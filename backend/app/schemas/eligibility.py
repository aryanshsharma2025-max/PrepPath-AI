from typing import List, Optional
from pydantic import BaseModel
from app.schemas.opportunity import RequirementExtraction, DocumentExtraction

class RequirementEvaluation(BaseModel):
    requirement: RequirementExtraction
    student_value: Optional[str] = None
    expected_value: Optional[str] = None
    result: str # PASS | FAIL | UNKNOWN
    explanation: str
    source_text: Optional[str] = None

class DocumentEvaluation(BaseModel):
    document: DocumentExtraction
    status: str # AVAILABLE | MISSING | OPTIONAL

class EligibilityResult(BaseModel):
    status: str # ELIGIBLE | INELIGIBLE | PARTIALLY_ELIGIBLE | UNKNOWN
    passed: List[RequirementEvaluation] = []
    failed: List[RequirementEvaluation] = []
    unknown: List[RequirementEvaluation] = []
    documents: List[DocumentEvaluation] = []
