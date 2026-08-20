from typing import Optional, List
from pydantic import BaseModel, Field

class StudentProfileBase(BaseModel):
    age: Optional[int] = None
    state: Optional[str] = None
    category: Optional[str] = None
    family_income: Optional[int] = None
    academic_percentage: Optional[float] = None
    academic_percentile: Optional[float] = None
    course_level: Optional[str] = None
    institution_type: Optional[str] = None
    institution_state: Optional[str] = None
    bpl_status: Optional[bool] = None
    receiving_other_scholarship: Optional[bool] = None
    passed_first_attempt: Optional[bool] = None
    attendance_status: Optional[str] = None
    attendance_percentage: Optional[float] = None

class StudentProfile(StudentProfileBase):
    id: str
    user_id: str

class StudentProfileUpdate(StudentProfileBase):
    pass

