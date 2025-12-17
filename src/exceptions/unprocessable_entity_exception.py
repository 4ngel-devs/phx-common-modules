"""Unprocessable Entity (422) exception for microservices."""

from typing import Any, List, Optional

from .business_exception import BusinessException


class UnprocessableEntityException(BusinessException):
    """
    Exception for unprocessable entity errors (HTTP 422).
    
    Use this when the request is well-formed but contains semantic errors
    or validation failures.
    
    Args:
        message: Human-readable error message
        process: Process or function where the error occurred (default: "Data Validation")
        errors: Optional list of detailed validation errors
    """

    def __init__(
        self,
        message: str,
        process: str = "Data Validation",
        errors: Optional[List[Any]] = None,
    ):
        """
        Initialize unprocessable entity exception.

        Args:
            message: Error message
            process: Process name where error occurred (default: "Data Validation")
            errors: Optional list of detailed validation errors
        """
        super().__init__(message, process, 422, errors)

