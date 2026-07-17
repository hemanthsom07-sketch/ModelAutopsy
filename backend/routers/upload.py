from fastapi import APIRouter, File, UploadFile

from backend.schemas.responses import UploadResponse
from backend.services.upload_service import handle_upload

router = APIRouter()


@router.post("/upload", response_model=UploadResponse, tags=["upload"])
async def upload_dataset(file: UploadFile = File(...)):
    """Accepts a .csv or .xlsx file, validates it, and returns an upload_id
    to use with /analyze, /predict, and /autopsy. Nothing is stored permanently."""
    return await handle_upload(file)
