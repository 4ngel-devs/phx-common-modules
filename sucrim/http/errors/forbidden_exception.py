"""Forbidden (403) exception for microservices."""

from typing import Any, List, Optional

from .business_exception import BusinessException


class ForbiddenException(BusinessException):
    """
    Exception for forbidden access errors (HTTP 403).
    
    Use this when the user is authenticated but doesn't have permission
    to perform the requested action.
    
    Args:
        message: Human-readable error message
        process: Process or function where the error occurred (default: "Authorization")
        errors: Optional list of detailed error information
    """

    def __init__(
        self,
        message: str,
        process: str = "Authorization",
        errors: Optional[List[Any]] = None,
    ):
        """
        Initialize forbidden exception.

        Args:
            message: Error message
            process: Process name where error occurred (default: "Authorization")
            errors: Optional list of detailed errors
        """
        super().__init__(message, process, 403, errors)

