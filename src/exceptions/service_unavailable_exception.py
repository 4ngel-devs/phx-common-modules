"""Service Unavailable (503) exception for microservices."""

from typing import Any, List, Optional

from .business_exception import BusinessException


class ServiceUnavailableException(BusinessException):
    """
    Exception for service unavailable errors (HTTP 503).
    
    Use this when the server is temporarily unable to handle the request
    (e.g., maintenance, overloaded).
    
    Args:
        message: Human-readable error message
        process: Process or function where the error occurred (default: "Service Availability")
        errors: Optional list of detailed error information
    """

    def __init__(
        self,
        message: str,
        process: str = "Service Availability",
        errors: Optional[List[Any]] = None,
    ):
        """
        Initialize service unavailable exception.

        Args:
            message: Error message
            process: Process name where error occurred (default: "Service Availability")
            errors: Optional list of detailed errors
        """
        super().__init__(message, process, 503, errors)

