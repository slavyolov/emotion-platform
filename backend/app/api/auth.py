from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class RegisterRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/register", response_model=TokenResponse)
async def register(payload: RegisterRequest):
    # MVP stub: accept any email/password and return fake token
    return TokenResponse(access_token="fake-token-for-" + payload.email)


@router.post("/login", response_model=TokenResponse)
async def login(payload: RegisterRequest):
    # MVP stub: accept any email/password and return fake token
    return TokenResponse(access_token="fake-token-for-" + payload.email)
