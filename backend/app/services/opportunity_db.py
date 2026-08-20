"""
Supabase Database Persistence for Opportunities & Requirements.
"""

import logging
from typing import Optional
from app.services.supabase import get_supabase_client
from app.schemas.opportunity import OpportunityExtraction

logger = logging.getLogger(__name__)

# Fallback in-memory database for testing when Supabase is unavailable
MOCK_OPPORTUNITIES_DB = {}
MOCK_ID_COUNTER = 1


def save_opportunity_to_db(opportunity: OpportunityExtraction) -> Optional[str]:
    """
    Save extracted opportunity and its eligibility requirements into Supabase database.
    Checks for existing title + provider duplicates before inserting.

    Parameters
    ----------
    opportunity : OpportunityExtraction
        Validated extraction output.

    Returns
    -------
    Optional[str]
        Stored opportunity ID if successful, or None if skipped/failed.
    """
    try:
        supabase = get_supabase_client()
    except Exception as err:
        logger.warning(f"Supabase client unavailable, skipping database persistence: {str(err)}")
        return None

    try:
        # Check for existing opportunity with same title and provider
        query = supabase.table("opportunities").select("id").eq("title", opportunity.title)
        if opportunity.provider:
            query = query.eq("provider", opportunity.provider)
        
        existing = query.execute()

        if existing.data and len(existing.data) > 0:
            opportunity_id = existing.data[0]["id"]
            logger.info(f"Existing opportunity found (ID: {opportunity_id}), skipping duplicate creation.")
            return opportunity_id

        # Insert new opportunity row
        opp_row = {
            "title": opportunity.title,
            "provider": opportunity.provider,
            "category": opportunity.category,
            "description": opportunity.description,
            "benefit": opportunity.benefit,
            "deadline": opportunity.deadline,
            "official_url": opportunity.official_url,
            "raw_extraction": opportunity.model_dump(mode="json"),
        }

        insert_res = supabase.table("opportunities").insert(opp_row).execute()
        if not insert_res.data:
            logger.warning("Supabase returned empty result on opportunity insert.")
            return None

        opportunity_id = insert_res.data[0]["id"]

        # Insert requirements rows
        if opportunity.eligibility:
            req_rows = []
            for req in opportunity.eligibility:
                req_rows.append({
                    "opportunity_id": opportunity_id,
                    "requirement_type": req.requirement_type,
                    "field": req.field,
                    "operator": req.operator,
                    "value": req.value,
                    "unit": req.unit,
                    "mandatory": req.mandatory,
                    "description": req.description,
                    "source_text": req.source_text,
                })
            
            if req_rows:
                supabase.table("requirements").insert(req_rows).execute()

        logger.info(f"Successfully stored opportunity '{opportunity.title}' (ID: {opportunity_id}) and requirements in Supabase.")
        return opportunity_id

    except Exception as err:
        logger.warning(f"Failed to persist opportunity to Supabase database: {str(err)}")
        
        # Fallback to in-memory store for MVP testing
        global MOCK_ID_COUNTER
        opportunity_id = str(MOCK_ID_COUNTER)
        MOCK_ID_COUNTER += 1
        MOCK_OPPORTUNITIES_DB[opportunity_id] = opportunity
        logger.info(f"Saved opportunity to MOCK_OPPORTUNITIES_DB with ID {opportunity_id}")
        return opportunity_id


def get_opportunity_from_db(opportunity_id: str) -> Optional[OpportunityExtraction]:
    """
    Retrieve an opportunity and its requirements from Supabase (or fallback mock).
    """
    if opportunity_id in MOCK_OPPORTUNITIES_DB:
        return MOCK_OPPORTUNITIES_DB[opportunity_id]
        
    try:
        supabase = get_supabase_client()
        res = supabase.table("opportunities").select("raw_extraction").eq("id", opportunity_id).execute()
        if res.data and len(res.data) > 0:
            raw_extraction = res.data[0].get("raw_extraction")
            if raw_extraction:
                return OpportunityExtraction(**raw_extraction)
    except Exception as err:
        logger.warning(f"Failed to retrieve opportunity from Supabase database: {str(err)}")
        
    return None
