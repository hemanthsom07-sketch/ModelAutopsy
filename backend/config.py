"""
Central configuration constants for the backend. Kept as plain values
(not a settings framework) since this is a single small deployment, not
a multi-environment service.
"""

PROJECT_NAME = "ModelAutopsy"
VERSION = "0.1"
DESCRIPTION = "Automatic dataset analysis and machine learning model autopsy platform."

ALLOWED_EXTENSIONS = {".csv", ".xlsx"}
MAX_UPLOAD_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB
UPLOAD_TTL_SECONDS = 30 * 60  # temporary uploads are cleaned up after 30 minutes
