"""Bad Request (400) exception for microservices."""

from typing import Any, List, Optional

from .business_exception import BusinessException


class BadRequestException(BusinessException):
    """
    Exception for bad request errors (HTTP 400).
    
    Use this for client errors where the request is malformed or invalid.
    
    Args:
        message: Human-readable error message
        process: Process or function where the error occurred (default: "Processing Client Request")
        errors: Optional list of detailed error information
    """

    def __init__(
        self,
        message: str,
        process: str = "Processing Client Request",
        errors: Optional[List[Any]] = None,
    ):
        """
        Initialize bad request exception.

        Args:
            message: Error message
            process: Process name where error occurred (default: "Processing Client Request")
            errors: Optional list of detailed errors
        """
        super().__init__(message, process, 400, errors)

