"""Conflict (409) exception for microservices."""

from typing import Any, List, Optional

from .business_exception import BusinessException


class ConflictException(BusinessException):
    """
    Exception for conflict errors (HTTP 409).
    
    Use this when the request conflicts with the current state of the resource
    (e.g., duplicate entry, concurrent modification).
    
    Args:
        message: Human-readable error message
        process: Process or function where the error occurred (default: "Resource Conflict")
        errors: Optional list of detailed error information
    """

    def __init__(
        self,
        message: str,
        process: str = "Resource Conflict",
        errors: Optional[List[Any]] = None,
    ):
        """
        Initialize conflict exception.

        Args:
            message: Error message
            process: Process name where error occurred (default: "Resource Conflict")
            errors: Optional list of detailed errors
        """
        super().__init__(message, process, 409, errors)

