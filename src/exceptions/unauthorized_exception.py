"""Unauthorized (401) exception for microservices."""

from typing import Any, List, Optional

from .business_exception import BusinessException


class UnauthorizedException(BusinessException):
    """
    Exception for unauthorized access errors (HTTP 401).
    
    Use this when authentication is required but missing or invalid.
    
    Args:
        message: Human-readable error message
        process: Process or function where the error occurred (default: "Authentication")
        errors: Optional list of detailed error information
    """

    def __init__(
        self,
        message: str,
        process: str = "Authentication",
        errors: Optional[List[Any]] = None,
    ):
        """
        Initialize unauthorized exception.

        Args:
            message: Error message
            process: Process name where error occurred (default: "Authentication")
            errors: Optional list of detailed errors
        """
        super().__init__(message, process, 401, errors)

