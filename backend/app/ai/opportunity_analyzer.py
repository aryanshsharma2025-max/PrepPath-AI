"""
AI Opportunity Analyzer Module.

Extracts structured scholarship criteria from raw PDF text using Gemini AI
and validates output against Pydantic schemas.
"""

import json
import logging
from typing import Optional
from app.ai.gemini import generate_structured
from app.schemas.opportunity import OpportunityExtraction

logger = logging.getLogger(__name__)

MAX_PROMPT_TEXT_LENGTH = 20000  # Character safeguard for Gemini input

SYSTEM_EXTRACTION_PROMPT = """You are an information extraction system.

Extract ONLY information explicitly supported by the provided opportunity document.

Do not invent eligibility criteria, deadlines, benefits, documents, URLs or requirements.

If information is absent, return null or an empty list.

Preserve the original meaning.

For every requirement, include source_text when possible.

Do not determine whether a particular student is eligible.
Your job is only to extract the opportunity's requirements.

### DOCUMENT EXTRACTION RULES:
1. Extract EVERY explicitly mentioned required document from the document text.
2. Separate each document into its own individual `DocumentExtraction` item (e.g. if the document says "Income Certificate, 12th Marksheet", extract "Income Certificate" as one item and "12th Marksheet" as a separate second item).
3. Search thoroughly for documents mentioned near phrases like:
   - "Required Documents"
   - "Documents Required"
   - "Documents Needed"
   - "Must submit"
   - "Applicants must provide"
   - "Upload the following"
   - "Please attach"
   - "Provide copy of"
4. NEVER invent or assume documents that are not present in the source document.
5. Extract and populate the `source_text` field for every extracted document with the exact snippet/sentence where it was mentioned.
6. Determine whether a document is mandatory or optional from context clues:
   - Mark as `mandatory: true` if the document is described as compulsory, mandatory, required, must, or no optional indicator is present.
   - Mark as `mandatory: false` only if the document is explicitly described as optional, if applicable, if available, or preferred.
7. If no documents are mentioned anywhere in the document text, return an empty list `[]` for `documents` rather than guessing.

Analyze the following document and extract structured JSON matching the requested schema:

--- DOCUMENT TEXT START ---
{document_text}
--- DOCUMENT TEXT END ---
"""


def analyze_opportunity_text(text: str) -> OpportunityExtraction:
    """
    Send extracted scholarship text to Gemini AI and return validated OpportunityExtraction schema.

    Parameters
    ----------
    text : str
        Cleaned text extracted from the opportunity document.

    Returns
    -------
    OpportunityExtraction
        Structured eligibility, document, and opportunity data.

    Raises
    ------
    ValueError
        If analysis or JSON validation fails.
    """
    if not text or not text.strip():
        raise ValueError("Cannot analyze empty document text.")

    # Apply text-size safeguard
    working_text = text.strip()
    if len(working_text) > MAX_PROMPT_TEXT_LENGTH:
        logger.warning(
            f"Extracted document text length ({len(working_text)} chars) exceeds limit ({MAX_PROMPT_TEXT_LENGTH}). Truncating safely."
        )
        working_text = working_text[:MAX_PROMPT_TEXT_LENGTH] + "\n\n[Document truncated for size]"

    formatted_prompt = SYSTEM_EXTRACTION_PROMPT.format(document_text=working_text)

    try:
        # Call Gemini structured output helper passing OpportunityExtraction model
        raw_json_response = generate_structured(
            prompt=formatted_prompt,
            response_schema=OpportunityExtraction,
        )
    except Exception as err:
        logger.error(f"Failed to communicate with Gemini AI: {str(err)}")
        raise ValueError(f"AI extraction failed: {str(err)}") from err

    if not raw_json_response:
        raise ValueError("Received empty response from AI model.")

    try:
        # Parse JSON and validate with Pydantic
        json_data = json.loads(raw_json_response)
        validated_opportunity = OpportunityExtraction.model_validate(json_data)
        return validated_opportunity
    except (json.JSONDecodeError, Exception) as err:
        logger.error(f"Failed to parse or validate Gemini structured output: {str(err)}")
        raise ValueError("AI produced invalid or malformed output structure.") from err
