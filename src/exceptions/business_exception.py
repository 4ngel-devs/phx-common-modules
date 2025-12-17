"""Business logic exception - main exception class for microservices."""

from typing import Any, List, Optional


class BusinessException(Exception):
    """
    Main exception class for business logic errors.
    
    This is the base exception class for all custom exceptions in this module.
    Use this for errors related to business rules, domain logic,
    or application-specific errors (e.g., "User not found", "Insufficient balance").
    
    All other exception classes inherit from this class to ensure
    consistent error handling across services.
    
    Args:
        message: Human-readable error message
        process: Process or function where the error occurred
        status_code: HTTP status code (default: 400)
        errors: Optional list of detailed error information
    """

    def __init__(
        self,
        message: str,
        process: str,
        status_code: int = 400,
        errors: Optional[List[Any]] = None,
    ):
        """
        Initialize business exception.

        Args:
            message: Error message
            process: Process name where error occurred
            status_code: HTTP status code (default: 400)
            errors: Optional list of detailed errors
        """
        super().__init__(message)
        self.message = message
        self.process = process
        self.status_code = status_code
        self.errors = errors or []

    def __str__(self) -> str:
        """String representation of the exception."""
        return f"{self.process}: {self.message}"

    def to_dict(self) -> dict:
        """
        Convert exception to dictionary for JSON responses.

        Returns:
            dict: Exception data as dictionary
        """
        return {
            "message": self.message,
            "process": self.process,
            "errors": self.errors,
        }

