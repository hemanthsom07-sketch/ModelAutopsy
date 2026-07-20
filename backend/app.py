"""
FastAPI entry point. Registers the routers and two exception handlers:

- ModelAutopsyError -> the clean, categorized errors raised deliberately
  throughout the backend (bad upload, missing target, etc.)
- ValueError -> a safety net for the few validation errors the src/
  engines themselves already raise (e.g. "Target column not found",
  "No usable feature columns remain") that aren't pre-checked separately
- Exception -> anything unexpected. Logged server-side; the client only
  ever sees a generic message, never a traceback.

Run from the project root (same convention as main.py):
    uvicorn backend.app:app --reload
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.config import DESCRIPTION, PROJECT_NAME, VERSION
from backend.routers import analyze, autopsy, predict, root, upload
from backend.utils.errors import ModelAutopsyError

app = FastAPI(title=PROJECT_NAME, version=VERSION, description=DESCRIPTION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "https://model-autopsy.vercel.app",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root.router)
app.include_router(upload.router)
app.include_router(analyze.router)
app.include_router(predict.router)
app.include_router(autopsy.router)


@app.exception_handler(ModelAutopsyError)
async def handle_model_autopsy_error(request: Request, exc: ModelAutopsyError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.error, "detail": exc.detail},
    )


@app.exception_handler(ValueError)
async def handle_value_error(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"error": "invalid_request", "detail": str(exc)},
    )


@app.exception_handler(Exception)
async def handle_unexpected_error(request: Request, exc: Exception):
    print(f"[ModelAutopsy] Unexpected error: {type(exc).__name__}: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_error",
            "detail": "An unexpected error occurred while processing the request.",
        },
    )
