"""
Handles upload validation, temporary storage, and cleanup.

Uploaded files are written to a dedicated OS temp directory (never inside
the project's own data/ folder) under a UUID-based filename, so an upload
can never collide with or overwrite another file. Each upload is tracked
in an in-memory registry keyed by that same UUID ("upload_id"); nothing
is persisted to a database. Expired uploads (older than
config.UPLOAD_TTL_SECONDS) are swept and deleted opportunistically each
time a new upload comes in - simple and dependency-free, appropriate for
a single-process demo backend.
"""

import tempfile
import time
import uuid
from pathlib import Path

from backend.config import ALLOWED_EXTENSIONS, MAX_UPLOAD_SIZE_BYTES, UPLOAD_TTL_SECONDS
from backend.schemas.responses import UploadResponse
from backend.utils.errors import ModelAutopsyError
from backend.utils.file_helpers import load_dataset

TEMP_UPLOAD_DIR = Path(tempfile.gettempdir()) / "modelautopsy_uploads"
TEMP_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

_UPLOAD_REGISTRY = {}  # upload_id -> {"path": Path, "created_at": float}


def _cleanup_expired_uploads():
    now = time.time()
    expired_ids = [
        upload_id
        for upload_id, entry in _UPLOAD_REGISTRY.items()
        if now - entry["created_at"] > UPLOAD_TTL_SECONDS
    ]
    for upload_id in expired_ids:
        entry = _UPLOAD_REGISTRY.pop(upload_id)
        entry["path"].unlink(missing_ok=True)


def get_upload_path(upload_id: str) -> Path:
    entry = _UPLOAD_REGISTRY.get(upload_id)
    if entry is None:
        raise ModelAutopsyError(
            "upload_not_found",
            f"No upload found for id '{upload_id}'. It may have expired - please upload the file again.",
            status_code=404,
        )
    return entry["path"]


async def handle_upload(file) -> UploadResponse:
    _cleanup_expired_uploads()

    original_name = file.filename or "upload"
    extension = Path(original_name).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ModelAutopsyError(
            "unsupported_file",
            f"Unsupported file extension '{extension}'. Only "
            f"{', '.join(sorted(ALLOWED_EXTENSIONS))} are supported.",
        )

    contents = await file.read()

    if len(contents) == 0:
        raise ModelAutopsyError("empty_file", "The uploaded file is empty.")

    if len(contents) > MAX_UPLOAD_SIZE_BYTES:
        raise ModelAutopsyError(
            "file_too_large",
            f"The uploaded file is {len(contents):,} bytes, which exceeds the "
            f"{MAX_UPLOAD_SIZE_BYTES:,} byte limit.",
        )

    upload_id = str(uuid.uuid4())
    temp_path = TEMP_UPLOAD_DIR / f"{upload_id}{extension}"
    temp_path.write_bytes(contents)

    try:
        data = load_dataset(str(temp_path))
    except ModelAutopsyError:
        temp_path.unlink(missing_ok=True)
        raise
    except Exception as exc:
        temp_path.unlink(missing_ok=True)
        raise ModelAutopsyError("invalid_file", f"Could not read the uploaded file: {exc}")

    if len(data) == 0:
        temp_path.unlink(missing_ok=True)
        raise ModelAutopsyError("empty_dataset", "The uploaded file has no data rows.")

    _UPLOAD_REGISTRY[upload_id] = {"path": temp_path, "created_at": time.time()}

    return UploadResponse(
        upload_id=upload_id,
        filename=original_name,
        file_size_bytes=len(contents),
        rows=len(data),
        columns=len(data.columns),
        column_names=[str(column) for column in data.columns],
    )
