from typing import Any, Dict, Optional


class SmartRecruitzError(Exception):
    """
    Base exception for all application-level errors.
    """

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(SmartRecruitzError):
    """Raised when validation fails."""

    def __init__(self, message: str, field: Optional[str] = None) -> None:
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            details={"field": field} if field else {},
        )


class DatabaseError(SmartRecruitzError):
    """Raised when a database operation fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message=message, code="DATABASE_ERROR")
