from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException
from pydantic import BaseModel

from app.api.auth import get_current_user, User
from app.services import emotion

router = APIRouter()


class Submission(BaseModel):
    id: str
    user_email: str
    name: str
    age: int
    gender: str
    location: Optional[str]
    country: str
    photo_filename: str
    primary_emotion: str
    emotion_scores: Dict[str, float]
    model_version: str


class SubmissionResponse(Submission):
    pass


# In-memory storage for MVP
_SUBMISSIONS: List[Submission] = []


@router.post("/", response_model=SubmissionResponse)
async def create_submission(
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    location: Optional[str] = Form(None),
    country: str = Form(...),
    photo: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """
    Create a submission: requires a valid JWT.
    Accepts multipart/form-data with a photo and metadata.
    """
    if age < 3 or age > 100:
        raise HTTPException(status_code=422, detail="Age out of range")

    submission_id = str(uuid4())
    image_bytes = await photo.read()

    emo = emotion.predict(image_bytes)

    submission = Submission(
        id=submission_id,
        user_email=current_user.email,
        name=name,
        age=age,
        gender=gender,
        location=location,
        country=country,
        photo_filename=photo.filename,
        primary_emotion=emo["primary_emotion"],
        emotion_scores=emo["scores"],
        model_version=emo["model_version"],
    )
    _SUBMISSIONS.append(submission)
    return submission
