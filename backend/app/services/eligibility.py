from typing import List, Any, Optional
import operator as op
from app.schemas.opportunity import RequirementExtraction, DocumentExtraction
from app.schemas.student import StudentProfileBase
from app.schemas.eligibility import EligibilityResult, RequirementEvaluation, DocumentEvaluation

# Mapping of requirement fields extracted by Gemini to StudentProfile fields.
# Covers common variant names Gemini may produce.
REQUIREMENT_FIELD_MAP = {
    # Age
    "age": "age",
    "minimum_age": "age",
    "maximum_age": "age",
    "age_limit": "age",
    # State / Domicile
    "state": "state",
    "domicile": "state",
    "domicile_state": "state",
    # Category / Caste
    "category": "category",
    "caste": "category",
    "caste_category": "category",
    # Family Income
    "family_income": "family_income",
    "annual_family_income": "family_income",
    "income": "family_income",
    "annual_income": "family_income",
    # Academic Percentage
    "minimum_percentage": "academic_percentage",
    "academic_percentage": "academic_percentage",
    "percentage": "academic_percentage",
    "marks_percentage": "academic_percentage",
    "minimum_marks": "academic_percentage",
    "annual_examination_marks": "academic_percentage",
    "examination_marks": "academic_percentage",
    # Academic Percentile
    "top_percentile": "academic_percentile",
    "percentile": "academic_percentile",
    "academic_percentile": "academic_percentile",
    "board_percentile": "academic_percentile",
    "minimum_percentile": "academic_percentile",
    # Course Level
    "course_level": "course_level",
    "course": "course_level",
    "course_type": "course_level",
    "degree": "course_level",
    "degree_level": "course_level",
    # Institution
    "institution": "institution_type",
    "institution_type": "institution_type",
    "college_type": "institution_type",
    # Institution State
    "institution_state": "institution_state",
    # BPL / Family Background
    "family_background": "bpl_status",
    "bpl_status": "bpl_status",
    "bpl": "bpl_status",
    "below_poverty_line": "bpl_status",
    "guardian_bpl_card": "bpl_status",
    "bpl_card": "bpl_status",
    # Other Scholarship
    "other_scholarship": "receiving_other_scholarship",
    "other_scholarships": "receiving_other_scholarship",
    "other_scholarship_exclusion": "receiving_other_scholarship",
    "receiving_other_scholarship": "receiving_other_scholarship",
    "other_scholarship_recipient": "receiving_other_scholarship",
    "other_scholarship_benefits": "receiving_other_scholarship",
    "no_other_scholarship": "receiving_other_scholarship",
    "no_other_scholarships": "receiving_other_scholarship",
    # Academic Performance / First Attempt
    "academic_performance": "passed_first_attempt",
    "exam_attempt": "passed_first_attempt",
    "pass_first_attempt": "passed_first_attempt",
    "first_attempt": "passed_first_attempt",
    # Explicit Attendance
    "attendance_percentage": "attendance_percentage",
    "attendance_percent": "attendance_percentage",
    "attendance_status": "attendance_status",
}

def resolve_requirement_field(req: RequirementExtraction) -> Optional[str]:
    """
    Resolve Gemini-extracted field name to StudentProfileBase field attribute.
    Differentiates numeric vs qualitative attendance requirements deterministically.
    """
    req_field_clean = req.field.lower().strip()
    
    # Explicit attendance fields
    if req_field_clean in ["attendance_percentage", "attendance_percent"]:
        return "attendance_percentage"
    if req_field_clean == "attendance_status":
        return "attendance_status"
        
    # Ambiguous attendance fields: 'attendance', 'minimum_attendance', 'attendance_criteria', 'attendance_requirement'
    if req_field_clean in [
        "attendance",
        "minimum_attendance",
        "attendance_criteria",
        "attendance_requirement",
        "attendance_rate"
    ]:
        val = str(req.value or "").strip()
        # A requirement is numeric if it contains digits or has '%' unit
        has_digit = any(c.isdigit() for c in val)
        is_pct_unit = bool(req.unit and "%" in req.unit)
        
        if has_digit or is_pct_unit:
            return "attendance_percentage"
        else:
            return "attendance_status"

    return REQUIREMENT_FIELD_MAP.get(req_field_clean)

def evaluate_condition(student_val: Any, operator_str: str, req_val: str) -> bool:
    if student_val is None:
        return False
        
    try:
        # Convert types based on student_val type
        if isinstance(student_val, bool):
            if req_val.lower() in ["true", "yes", "bpl", "no other scholarship"]:
                parsed_req = True
            elif req_val.lower() in ["false", "no"]:
                parsed_req = False
            else:
                # Custom logic for bpl / other_scholarship
                if "bpl" in req_val.lower():
                    parsed_req = True
                elif "first attempt" in req_val.lower() or "pass" in req_val.lower():
                    parsed_req = True
                elif "no shortage" in req_val.lower() or "adequate" in req_val.lower() or "sufficient" in req_val.lower() or "not shorten" in req_val.lower():
                    parsed_req = True
                else:
                    parsed_req = req_val.lower() == 'true'
            return student_val == parsed_req if operator_str in ["==", "="] else student_val != parsed_req
            
        elif isinstance(student_val, (int, float)):
            # Clean requirement value for numbers (e.g. remove commas, currency, %)
            clean_req = ''.join(c for c in req_val if c.isdigit() or c == '.')
            if not clean_req:
                return False
            parsed_req = float(clean_req)
            
            # If requirement is given as decimal fraction e.g. 0.75 while student percentage is in 0..100
            if 0.0 < parsed_req <= 1.0 and student_val > 1.0:
                parsed_req = parsed_req * 100.0
            
            ops = {
                "==": op.eq, "=": op.eq,
                "!=": op.ne,
                ">": op.gt,
                ">=": op.ge,
                "<": op.lt,
                "<=": op.le
            }
            if operator_str in ops:
                return ops[operator_str](student_val, parsed_req)
            return student_val == parsed_req
                
        elif isinstance(student_val, str):
            student_val_lower = student_val.lower().strip()
            req_val_lower = req_val.lower().strip()

            # Qualitative attendance / conduct matching
            positive_qualitative = ["adequate", "regular", "good", "satisfactory", "sufficient", "no shortage", "not shorten", "proper"]
            if any(q in student_val_lower for q in positive_qualitative) and any(q in req_val_lower for q in positive_qualitative):
                return True

            if operator_str in ["==", "="]:
                return student_val_lower == req_val_lower or req_val_lower in student_val_lower or student_val_lower in req_val_lower
            elif operator_str == "!=":
                return student_val_lower != req_val_lower and req_val_lower not in student_val_lower
            elif operator_str == "in":
                parts = [p.strip() for p in req_val_lower.replace('/', ',').replace(' or ', ',').split(',') if p.strip()]
                return any(p == student_val_lower or p in student_val_lower or student_val_lower in p for p in parts)
            elif operator_str == "not_in":
                parts = [p.strip() for p in req_val_lower.replace('/', ',').replace(' or ', ',').split(',') if p.strip()]
                return not any(p == student_val_lower or p in student_val_lower or student_val_lower in p for p in parts)
                
    except Exception:
        pass
        
    # Fallback string comparison
    if operator_str in ["==", "="]:
        return str(student_val).lower().strip() == req_val.lower().strip()
    return False

def evaluate_eligibility(requirements: List[RequirementExtraction], documents: List[DocumentExtraction], student: StudentProfileBase) -> EligibilityResult:
    passed = []
    failed = []
    unknown = []
    
    # Evaluate Requirements
    for req in requirements:
        mapped_field = resolve_requirement_field(req)
        
        if not mapped_field:
            unknown.append(RequirementEvaluation(
                requirement=req,
                student_value=None,
                expected_value=req.value,
                result="UNKNOWN",
                explanation=f"Requirement '{req.field}' is not currently supported by the eligibility engine.",
                source_text=req.source_text
            ))
            continue
            
        student_val = getattr(student, mapped_field, None)
        
        if student_val is None:
            unknown.append(RequirementEvaluation(
                requirement=req,
                student_value=None,
                expected_value=req.value,
                result="UNKNOWN",
                explanation=f"Student profile is missing information for {mapped_field}.",
                source_text=req.source_text
            ))
            continue
            
        operator_str = req.operator or "=="
        
        # Special case mapping to bools for certain fields
        if mapped_field == "receiving_other_scholarship":
            req_val_str = str(req.value or "").lower()
            if student_val is False and (
                "no" in req_val_str or "none" in req_val_str or "any" in req_val_str or "false" in req_val_str or operator_str in ["not_in", "!="]
            ):
                is_pass = True
            elif student_val is True and (
                "no" in req_val_str or "none" in req_val_str or "any" in req_val_str or "false" in req_val_str or operator_str in ["not_in", "!="]
            ):
                is_pass = False
            else:
                is_pass = evaluate_condition(student_val, operator_str, req.value or "")
        elif mapped_field == "passed_first_attempt":
            if student_val is True:
                is_pass = True
            else:
                is_pass = False
        elif mapped_field == "bpl_status":
            if student_val is True:
                is_pass = True
            else:
                is_pass = False
        else:
            is_pass = evaluate_condition(student_val, operator_str, req.value or "")
            
        eval_result = RequirementEvaluation(
            requirement=req,
            student_value=str(student_val),
            expected_value=req.value,
            result="PASS" if is_pass else "FAIL",
            explanation=f"Student value '{student_val}' {'meets' if is_pass else 'does not meet'} criteria '{req.operator or '=='} {req.value}'",
            source_text=req.source_text
        )
        
        if is_pass:
            passed.append(eval_result)
        else:
            failed.append(eval_result)

    # Calculate overall status
    # Any mandatory FAIL -> INELIGIBLE
    # All mandatory PASS -> ELIGIBLE
    # No mandatory FAIL, but some mandatory UNKNOWN -> UNKNOWN
    
    mandatory_failed = [r for r in failed if r.requirement.mandatory]
    mandatory_unknown = [r for r in unknown if r.requirement.mandatory]
    
    if mandatory_failed:
        overall_status = "INELIGIBLE"
    elif mandatory_unknown:
        overall_status = "UNKNOWN"
    else:
        overall_status = "ELIGIBLE"
        
    # Evaluate Documents (Checklist representation)
    doc_evals = []
    for doc in documents:
        status = "REQUIRED" if doc.mandatory else "OPTIONAL"
        doc_evals.append(DocumentEvaluation(document=doc, status=status))

    return EligibilityResult(
        status=overall_status,
        passed=passed,
        failed=failed,
        unknown=unknown,
        documents=doc_evals
    )

