from typing import Optional

from pydantic import BaseModel


class UploadRequest(BaseModel):
    """
    Body for /analyze, /predict, and /autopsy - all three operate on a
    dataset that was already uploaded via POST /upload.

    target_column is optional here because /analyze can run without one;
    /predict and /autopsy require it and will return a clean
    missing_target_column error if it is left out.
    """
    upload_id: str
    target_column: Optional[str] = None
