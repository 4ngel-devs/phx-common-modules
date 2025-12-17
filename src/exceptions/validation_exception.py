"""Validation exceptions for microservices."""

from typing import Any, List, Optional

from .business_exception import BusinessException


class ValidationException(BusinessException):
    """
    Exception for validation errors.
    
    Use this for input validation errors, data format errors,
    or constraint violations (e.g., "Invalid email format", "Required field missing").
    
    Args:
        message: Human-readable error message
        process: Process or function where the error occurred
        status_code: HTTP status code (default: 422)
        errors: Optional list of detailed validation errors
    """

    def __init__(
        self,
        message: str,
        process: str,
        status_code: int = 422,
        errors: Optional[List[Any]] = None,
    ):
        """
        Initialize validation exception.

        Args:
            message: Error message
            process: Process name where error occurred
            status_code: HTTP status code (default: 422)
            errors: Optional list of detailed validation errors
        """
        super().__init__(message, process, status_code, errors)

