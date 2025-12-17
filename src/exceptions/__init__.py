"""Exception classes for microservices.

BusinessException is the main exception class and base for all other exceptions.
All other exceptions inherit from BusinessException and provide
specific HTTP status codes for different error scenarios.
"""

from .bad_request_exception import BadRequestException
from .business_exception import BusinessException
from .conflict_exception import ConflictException
from .forbidden_exception import ForbiddenException
from .internal_server_error_exception import InternalServerErrorException
from .not_found_exception import NotFoundException
from .service_unavailable_exception import ServiceUnavailableException
from .unauthorized_exception import UnauthorizedException
from .unprocessable_entity_exception import UnprocessableEntityException
from .validation_exception import ValidationException

__all__ = [
    "BusinessException",  # Main exception class - base for all other exceptions
    "ValidationException",
    "BadRequestException",
    "UnauthorizedException",
    "ForbiddenException",
    "NotFoundException",
    "ConflictException",
    "UnprocessableEntityException",
    "InternalServerErrorException",
    "ServiceUnavailableException",
]
