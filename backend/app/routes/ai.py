from fastapi import APIRouter
from app.ai.gemini import generate_text

router = APIRouter(prefix="/api/ai", tags=["AI"])


@router.get("/test")
def test_gemini_connection():
    """
    Temporary development endpoint to test Gemini API connection.
    Sends a lightweight prompt and returns the result.
    """
    prompt = "Reply with exactly: PrepPath AI Gemini connection successful."
    
    try:
        response_text = generate_text(prompt=prompt)
        return {
            "success": True,
            "response": response_text.strip()
        }
    except Exception as err:
        return {
            "success": False,
            "error": f"Gemini service unavailable: {str(err)}"
        }
