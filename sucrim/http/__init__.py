"""HTTP utilities for Phoenix microservices."""

from .exception_handlers import setup_exception_handlers

# Re-export errors and responses for convenience
from .errors import (
    BadRequestException,
    BusinessException,
    ConflictException,
    ForbiddenException,
    InternalServerErrorException,
    NotFoundException,
    ServiceUnavailableException,
    UnauthorizedException,
    UnprocessableEntityException,
    ValidationException,
)
from .response import ApiResponseDto

__all__ = [
    "setup_exception_handlers",
    "BusinessException",
    "ValidationException",
    "BadRequestException",
    "UnauthorizedException",
    "ForbiddenException",
    "NotFoundException",
    "ConflictException",
    "UnprocessableEntityException",
    "InternalServerErrorException",
    "ServiceUnavailableException",
    "ApiResponseDto",
]
