from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from app.schemas.student import StudentProfile, StudentProfileUpdate

router = APIRouter(prefix="/api/profile", tags=["Student Profile"])

# Mock authenticated user ID since full auth is not yet implemented in frontend
def get_current_user_id() -> str:
    return "test-student-123"

# In-memory store for MVP if Supabase fails
MOCK_DB = {}

@router.get("", response_model=StudentProfile)
def get_profile(user_id: str = Depends(get_current_user_id)):
    """Get the current student profile."""
    # In a real app with Supabase Auth:
    # client = get_supabase_client()
    # res = client.table("students").select("*").eq("user_id", user_id).execute()
    # if res.data: return StudentProfile(**res.data[0])
    
    if user_id in MOCK_DB:
        return MOCK_DB[user_id]
        
    # Return empty profile if not found
    return StudentProfile(id="mock-id", user_id=user_id)

@router.post("", response_model=StudentProfile)
def update_profile(profile_update: StudentProfileUpdate, user_id: str = Depends(get_current_user_id)):
    """Create or update the student profile."""
    
    # In a real app, persist to Supabase
    profile = StudentProfile(
        id="mock-id",
        user_id=user_id,
        **profile_update.model_dump(exclude_unset=True)
    )
    MOCK_DB[user_id] = profile
    return profile
