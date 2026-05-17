from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import APIRouter, File, Form, UploadFile, HTTPException, Header
from pydantic import BaseModel

from app.services import emotion

router = APIRouter()


class Submission(BaseModel):
    id: str
    user_token: str
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


_SUBMISSIONS: List[Submission] = []


@router.post("/", response_model=SubmissionResponse)
async def create_submission(
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    location: Optional[str] = Form(None),
    country: str = Form(...),
    photo: UploadFile = File(...),
    authorization: str = Header("", alias="Authorization"),
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    if age < 3 or age > 100:
        raise HTTPException(status_code=422, detail="Age out of range")

    submission_id = str(uuid4())
    image_bytes = await photo.read()
    emo = emotion.predict(image_bytes)

    submission = Submission(
        id=submission_id,
        user_token=authorization,
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
