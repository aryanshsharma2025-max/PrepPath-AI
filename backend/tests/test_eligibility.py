import pytest
from app.schemas.opportunity import RequirementExtraction
from app.schemas.student import StudentProfile
from app.services.eligibility import evaluate_eligibility

def create_req(field, operator, value, mandatory=True):
    return RequirementExtraction(
        requirement_type="demographic",
        field=field,
        operator=operator,
        value=value,
        unit="",
        mandatory=mandatory,
        description=f"{field} {operator} {value}",
        source_text="Sample text"
    )

def test_income_pass():
    reqs = [create_req("family_income", "<=", "450000")]
    student = StudentProfile(id="1", user_id="1", family_income=300000)
    result = evaluate_eligibility(reqs, [], student)
    assert result.status == "ELIGIBLE"
    assert len(result.passed) == 1
    assert result.passed[0].requirement.field == "family_income"

def test_income_fail():
    reqs = [create_req("family_income", "<=", "450000")]
    student = StudentProfile(id="1", user_id="1", family_income=600000)
    result = evaluate_eligibility(reqs, [], student)
    assert result.status == "INELIGIBLE"
    assert len(result.failed) == 1

def test_missing_income_unknown():
    reqs = [create_req("family_income", "<=", "450000")]
    student = StudentProfile(id="1", user_id="1", family_income=None)
    result = evaluate_eligibility(reqs, [], student)
    assert result.status == "UNKNOWN"
    assert len(result.unknown) == 1

def test_percentage_pass():
    reqs = [create_req("academic_percentage", ">=", "75")]
    student = StudentProfile(id="1", user_id="1", academic_percentage=80)
    result = evaluate_eligibility(reqs, [], student)
    assert result.status == "ELIGIBLE"
    assert len(result.passed) == 1

def test_percentage_fail():
    reqs = [create_req("academic_percentage", ">=", "75")]
    student = StudentProfile(id="1", user_id="1", academic_percentage=60)
    result = evaluate_eligibility(reqs, [], student)
    assert result.status == "INELIGIBLE"
    assert len(result.failed) == 1

def test_bpl_pass():
    reqs = [create_req("bpl_status", "==", "true")]
    student = StudentProfile(id="1", user_id="1", bpl_status=True)
    result = evaluate_eligibility(reqs, [], student)
    assert result.status == "ELIGIBLE"

def test_bpl_fail():
    reqs = [create_req("bpl_status", "==", "true")]
    student = StudentProfile(id="1", user_id="1", bpl_status=False)
    result = evaluate_eligibility(reqs, [], student)
    assert result.status == "INELIGIBLE"

def test_institution_pass():
    reqs = [create_req("institution_type", "==", "Government")]
    student = StudentProfile(id="1", user_id="1", institution_type="Government")
    result = evaluate_eligibility(reqs, [], student)
    assert result.status == "ELIGIBLE"

def test_other_scholarship_restriction():
    reqs = [create_req("other_scholarship", "==", "False")]
    # If the requirement says they cannot have another scholarship
    student_pass = StudentProfile(id="1", user_id="1", receiving_other_scholarship=False)
    result_pass = evaluate_eligibility(reqs, [], student_pass)
    assert result_pass.status == "ELIGIBLE"
    
    student_fail = StudentProfile(id="1", user_id="1", receiving_other_scholarship=True)
    result_fail = evaluate_eligibility(reqs, [], student_fail)
    assert result_fail.status == "INELIGIBLE"

def test_first_attempt_requirement():
    reqs = [create_req("academic_performance", "==", "Pass in first attempt")]
    student_pass = StudentProfile(id="1", user_id="1", passed_first_attempt=True)
    assert evaluate_eligibility(reqs, [], student_pass).status == "ELIGIBLE"

    student_fail = StudentProfile(id="1", user_id="1", passed_first_attempt=False)
    assert evaluate_eligibility(reqs, [], student_fail).status == "INELIGIBLE"

def test_mandatory_failure_ineligible():
    reqs = [
        create_req("family_income", "<=", "450000", mandatory=True),
        create_req("academic_percentage", ">=", "75", mandatory=True)
    ]
    student = StudentProfile(id="1", user_id="1", family_income=300000, academic_percentage=60)
    result = evaluate_eligibility(reqs, [], student)
    assert result.status == "INELIGIBLE"

def test_mandatory_unknown_unknown():
    reqs = [
        create_req("family_income", "<=", "450000", mandatory=True),
        create_req("academic_percentage", ">=", "75", mandatory=True)
    ]
    student = StudentProfile(id="1", user_id="1", family_income=300000, academic_percentage=None)
    result = evaluate_eligibility(reqs, [], student)
    assert result.status == "UNKNOWN"

def test_all_mandatory_pass_eligible():
    reqs = [
        create_req("family_income", "<=", "450000", mandatory=True),
        create_req("academic_percentage", ">=", "75", mandatory=True)
    ]
    student = StudentProfile(id="1", user_id="1", family_income=300000, academic_percentage=80)
    result = evaluate_eligibility(reqs, [], student)
    assert result.status == "ELIGIBLE"

def test_optional_failure_does_not_make_ineligible():
    reqs = [
        create_req("family_income", "<=", "450000", mandatory=True),
        create_req("bpl_status", "==", "true", mandatory=False)
    ]
    student = StudentProfile(id="1", user_id="1", family_income=300000, bpl_status=False)
    result = evaluate_eligibility(reqs, [], student)
    assert result.status == "ELIGIBLE"
    assert len(result.failed) == 1

def test_unmapped_requirement_unknown():
    reqs = [create_req("unmapped_unknown_field", "==", "value")]
    student = StudentProfile(id="1", user_id="1")
    result = evaluate_eligibility(reqs, [], student)
    assert result.status == "UNKNOWN"
    assert len(result.unknown) == 1

def test_attendance_percentage_pass():
    reqs = [create_req("attendance_percentage", ">=", "75")]
    student = StudentProfile(id="1", user_id="1", attendance_percentage=82.0)
    result = evaluate_eligibility(reqs, [], student)
    assert result.status == "ELIGIBLE"
    assert len(result.passed) == 1
    assert result.passed[0].result == "PASS"

def test_attendance_percentage_fail():
    reqs = [create_req("attendance_percentage", ">=", "75")]
    student = StudentProfile(id="1", user_id="1", attendance_percentage=60.0)
    result = evaluate_eligibility(reqs, [], student)
    assert result.status == "INELIGIBLE"
    assert len(result.failed) == 1
    assert result.failed[0].result == "FAIL"

def test_attendance_percentage_missing_unknown():
    reqs = [create_req("attendance_percentage", ">=", "75")]
    student = StudentProfile(id="1", user_id="1", attendance_percentage=None)
    result = evaluate_eligibility(reqs, [], student)
    assert result.status == "UNKNOWN"
    assert len(result.unknown) == 1
    assert result.unknown[0].result == "UNKNOWN"

def test_ambiguous_attendance_numeric_routes_to_percentage():
    # When Gemini outputs field="attendance" with numeric value/operator
    reqs = [create_req("attendance", ">=", "75")]
    student_pass = StudentProfile(id="1", user_id="1", attendance_percentage=82.0, attendance_status="adequate")
    result_pass = evaluate_eligibility(reqs, [], student_pass)
    assert result_pass.status == "ELIGIBLE"
    assert len(result_pass.passed) == 1
    assert "82" in result_pass.passed[0].explanation

    student_fail = StudentProfile(id="1", user_id="1", attendance_percentage=60.0, attendance_status="adequate")
    result_fail = evaluate_eligibility(reqs, [], student_fail)
    assert result_fail.status == "INELIGIBLE"
    assert len(result_fail.failed) == 1

def test_qualitative_attendance_does_not_convert_to_number():
    # When Gemini outputs field="attendance" with qualitative requirement like "adequate"
    reqs = [create_req("attendance", "==", "adequate")]
    # Student has adequate status but no numeric attendance
    student = StudentProfile(id="1", user_id="1", attendance_status="adequate", attendance_percentage=None)
    result = evaluate_eligibility(reqs, [], student)
    assert result.status == "ELIGIBLE"
    assert len(result.passed) == 1
    assert result.passed[0].result == "PASS"

def test_explicit_attendance_status_uses_status():
    reqs = [create_req("attendance_status", "==", "adequate")]
    student_match = StudentProfile(id="1", user_id="1", attendance_status="adequate")
    assert evaluate_eligibility(reqs, [], student_match).status == "ELIGIBLE"

    student_diff = StudentProfile(id="1", user_id="1", attendance_status="poor")
    assert evaluate_eligibility(reqs, [], student_diff).status == "INELIGIBLE"

def test_explicit_attendance_percentage_uses_percentage():
    reqs = [create_req("attendance_percentage", ">=", "75")]
    student = StudentProfile(id="1", user_id="1", attendance_percentage=75.0)
    result = evaluate_eligibility(reqs, [], student)
    assert result.status == "ELIGIBLE"
    assert len(result.passed) == 1

