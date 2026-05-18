from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, submissions, admin

app = FastAPI(title="Emotion Classification API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": "Emotion Platform API is running",
        "docs": "/docs",
        "health": "/health",
    }

@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(submissions.router, prefix="/api/v1/submissions", tags=["submissions"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])