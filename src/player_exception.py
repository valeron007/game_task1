from typing import Any

class PlayerException(Exception):
    """Exception raised for custom error in the application."""

    def __init__(self, message: str, error_code: Any):
        super().__init__(message)
        self.error_code = error_code        

    def __str__(self) -> str:
        return f"{self.message} (Error Code: {self.error_code})"
