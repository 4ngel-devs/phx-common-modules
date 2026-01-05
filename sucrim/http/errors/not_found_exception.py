"""Not Found (404) exception for microservices."""

from typing import Any, List, Optional

from .business_exception import BusinessException


class NotFoundException(BusinessException):
    """
    Exception for resource not found errors (HTTP 404).
    
    Use this when a requested resource doesn't exist.
    
    Args:
        message: Human-readable error message
        process: Process or function where the error occurred (default: "Resource Lookup")
        errors: Optional list of detailed error information
    """

    def __init__(
        self,
        message: str,
        process: str = "Resource Lookup",
        errors: Optional[List[Any]] = None,
    ):
        """
        Initialize not found exception.

        Args:
            message: Error message
            process: Process name where error occurred (default: "Resource Lookup")
            errors: Optional list of detailed errors
        """
        super().__init__(message, process, 404, errors)

