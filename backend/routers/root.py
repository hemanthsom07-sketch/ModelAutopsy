from fastapi import APIRouter

from backend.config import PROJECT_NAME, VERSION
from backend.schemas.responses import RootResponse

router = APIRouter()


@router.get("/", response_model=RootResponse, tags=["root"])
def read_root():
    return RootResponse(project_name=PROJECT_NAME, version=VERSION, status="ok")
