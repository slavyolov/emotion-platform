from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from .submissions import Submission, _SUBMISSIONS

router = APIRouter()


@router.get("/submissions", response_model=List[Submission])
async def list_submissions(
    emotion: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
):
    results = _SUBMISSIONS
    if emotion:
        results = [s for s in results if s.primary_emotion == emotion]
    if country:
        results = [s for s in results if s.country == country]
    return results


@router.get("/submissions/{submission_id}", response_model=Submission)
async def get_submission(submission_id: str):
    for s in _SUBMISSIONS:
        if s.id == submission_id:
            return s
    raise HTTPException(status_code=404, detail="Not found")
