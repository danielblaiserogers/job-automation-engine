from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.job import JobListing
from app.services.adzuna_client import AdzunaClient

router = APIRouter(prefix="/jobs", tags=["Jobs"])

# Keep this decorator:
# @router.post("/fetch")

# Add this decorator:
@router.get("/fetch")
@router.post("/fetch")
async def fetch_and_store_jobs(
    query: str = Query(default=""),
    location: str = Query(default="28716"),
    session: Session = Depends(get_session)
):
    try:
        raw_jobs = await AdzunaClient.fetch_jobs(query=query, location=location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to query upstream API: {str(e)}")

    added_count = 0
    for item in raw_jobs:
        ext_id = str(item.get("id"))
        
        # Deduplication check
        existing = session.exec(select(JobListing).where(JobListing.external_id == ext_id)).first()
        if not existing:
            job = JobListing(
                external_id=ext_id,
                title=item.get("title", "N/A"),
                company=item.get("company", {}).get("display_name", "Unknown"),
                location=item.get("location", {}).get("display_name", "Remote"),
                description=item.get("description", ""),
                url=item.get("redirect_url", "")
            )
            session.add(job)
            added_count += 1

    session.commit()
    return {"status": "success", "new_jobs_added": added_count}

@router.get("/", response_model=list[JobListing])
def get_jobs(session: Session = Depends(get_session)):
    return session.exec(select(JobListing)).all()