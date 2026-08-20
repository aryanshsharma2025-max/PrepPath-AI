from fastapi import APIRouter, File, UploadFile, status, Depends
from fastapi.responses import JSONResponse
from app.services.pdf import extract_text_from_pdf_bytes
from app.ai.opportunity_analyzer import analyze_opportunity_text
from app.services.opportunity_db import save_opportunity_to_db, get_opportunity_from_db
from app.services.eligibility import evaluate_eligibility
from app.routes.profile import get_current_user_id, MOCK_DB
from app.schemas.student import StudentProfile
from app.schemas.eligibility import EligibilityResult

router = APIRouter(prefix="/api/opportunities", tags=["Opportunities"])


@router.post("/analyze")
async def analyze_opportunity(file: UploadFile = File(...)):
    """
    Analyze uploaded Scholarship PDF document.
    Extracts text, parses structured criteria via Gemini AI, stores in Supabase, and returns JSON.
    """
    if not file or not file.filename:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"success": False, "error": "No file uploaded. Please select a PDF file."}
        )

    # Validate file extension
    filename = file.filename.lower()
    if not filename.endswith(".pdf"):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"success": False, "error": "Invalid file type. Only PDF documents (.pdf) are supported."}
        )

    try:
        pdf_bytes = await file.read()
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"success": False, "error": "Failed to read uploaded file contents."}
        )

    # Step 1: Extract PDF text
    try:
        extracted_text = extract_text_from_pdf_bytes(pdf_bytes)
    except ValueError as err:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"success": False, "error": str(err)}
        )
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"success": False, "error": "An error occurred while processing the PDF file."}
        )

    # Step 2: Extract structured criteria with Gemini AI
    try:
        opportunity = analyze_opportunity_text(extracted_text)
    except ValueError as err:
        return JSONResponse(
            status_code=422,
            content={"success": False, "error": str(err)}
        )
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"success": False, "error": "Failed to analyze document with AI service."}
        )

    # Step 3: Persist to Supabase database (or fallback)
    opportunity_id = save_opportunity_to_db(opportunity)

    # Step 4: Return structured result
    res = opportunity.model_dump(mode="json")
    if opportunity_id:
        res["id"] = opportunity_id
        
    return {
        "success": True,
        "opportunity": res
    }

@router.post("/{opportunity_id}/eligibility", response_model=EligibilityResult)
def evaluate_student_eligibility(opportunity_id: str, user_id: str = Depends(get_current_user_id)):
    """
    Evaluates the authenticated student's profile against the stored opportunity requirements deterministically.
    """
    # 1. Fetch opportunity
    opportunity = get_opportunity_from_db(opportunity_id)
    if not opportunity:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"success": False, "error": f"Opportunity {opportunity_id} not found."}
        )
        
    # 2. Fetch student profile
    # In a real app, query Supabase. For MVP, use Mock
    if user_id in MOCK_DB:
        student = MOCK_DB[user_id]
    else:
        # Default empty profile
        student = StudentProfile(id="mock-id", user_id=user_id)
        
    # 3. Evaluate deterministic engine
    result = evaluate_eligibility(
        requirements=opportunity.eligibility or [],
        documents=opportunity.documents or [],
        student=student
    )
    
    return result
