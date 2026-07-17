"""
A single custom exception type for all KNOWN, user-facing API errors, so
every error response has the same {"error": ..., "detail": ...} shape.
Unexpected exceptions are caught separately in app.py and never reach the
client as a raw traceback.
"""


class ModelAutopsyError(Exception):
    def __init__(self, error: str, detail: str, status_code: int = 400):
        self.error = error
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)
