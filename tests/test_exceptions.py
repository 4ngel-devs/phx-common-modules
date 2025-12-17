"""Tests for exception classes."""

import pytest

from src.exceptions import (
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


class TestBusinessExceptionBase:
    """Test cases for BusinessException base functionality."""

    def test_business_exception_initialization(self):
        """Test that business exception initializes correctly."""
        exc = BusinessException(
            message="Test error",
            process="test_process",
            status_code=500,
        )

        assert exc.message == "Test error"
        assert exc.process == "test_process"
        assert exc.status_code == 500
        assert exc.errors == []

    def test_business_exception_with_errors(self):
        """Test business exception with error details."""
        errors = [{"field": "email", "message": "Invalid format"}]
        exc = BusinessException(
            message="Validation failed",
            process="validation",
            status_code=422,
            errors=errors,
        )

        assert exc.errors == errors
        assert len(exc.errors) == 1

    def test_business_exception_str_representation(self):
        """Test string representation of business exception."""
        exc = BusinessException(
            message="Test error",
            process="test_process",
        )

        assert str(exc) == "test_process: Test error"

    def test_business_exception_to_dict(self):
        """Test converting exception to dictionary."""
        errors = [{"field": "email", "message": "Invalid"}]
        exc = BusinessException(
            message="Test error",
            process="test_process",
            status_code=400,
            errors=errors,
        )

        result = exc.to_dict()

        assert result["message"] == "Test error"
        assert result["process"] == "test_process"
        assert result["errors"] == errors

    def test_business_exception_inherits_from_exception(self):
        """Test that business exception inherits from Exception."""
        exc = BusinessException(
            message="Test",
            process="test",
        )

        assert isinstance(exc, Exception)


class TestBadRequestException:
    """Test cases for BadRequestException."""

    def test_bad_request_exception_default_status_code(self):
        """Test that BadRequestException has correct default status code."""
        exc = BadRequestException(message="Invalid request")

        assert exc.status_code == 400
        assert exc.message == "Invalid request"
        assert exc.process == "Processing Client Request"

    def test_bad_request_exception_custom_process(self):
        """Test BadRequestException with custom process."""
        exc = BadRequestException(
            message="Invalid request",
            process="custom_process",
        )

        assert exc.status_code == 400
        assert exc.process == "custom_process"

    def test_bad_request_exception_with_errors(self):
        """Test BadRequestException with error details."""
        errors = [{"field": "id", "message": "Invalid format"}]
        exc = BadRequestException(
            message="Invalid request",
            errors=errors,
        )

        assert exc.errors == errors


class TestUnauthorizedException:
    """Test cases for UnauthorizedException."""

    def test_unauthorized_exception_default_status_code(self):
        """Test that UnauthorizedException has correct default status code."""
        exc = UnauthorizedException(message="Not authenticated")

        assert exc.status_code == 401
        assert exc.process == "Authentication"

    def test_unauthorized_exception_custom_process(self):
        """Test UnauthorizedException with custom process."""
        exc = UnauthorizedException(
            message="Not authenticated",
            process="token_validation",
        )

        assert exc.status_code == 401
        assert exc.process == "token_validation"


class TestForbiddenException:
    """Test cases for ForbiddenException."""

    def test_forbidden_exception_default_status_code(self):
        """Test that ForbiddenException has correct default status code."""
        exc = ForbiddenException(message="Access denied")

        assert exc.status_code == 403
        assert exc.process == "Authorization"

    def test_forbidden_exception_custom_process(self):
        """Test ForbiddenException with custom process."""
        exc = ForbiddenException(
            message="Access denied",
            process="permission_check",
        )

        assert exc.status_code == 403
        assert exc.process == "permission_check"


class TestNotFoundException:
    """Test cases for NotFoundException."""

    def test_not_found_exception_default_status_code(self):
        """Test that NotFoundException has correct default status code."""
        exc = NotFoundException(message="Resource not found")

        assert exc.status_code == 404
        assert exc.process == "Resource Lookup"

    def test_not_found_exception_custom_process(self):
        """Test NotFoundException with custom process."""
        exc = NotFoundException(
            message="User not found",
            process="user_lookup",
        )

        assert exc.status_code == 404
        assert exc.process == "user_lookup"


class TestConflictException:
    """Test cases for ConflictException."""

    def test_conflict_exception_default_status_code(self):
        """Test that ConflictException has correct default status code."""
        exc = ConflictException(message="Resource conflict")

        assert exc.status_code == 409
        assert exc.process == "Resource Conflict"

    def test_conflict_exception_with_errors(self):
        """Test ConflictException with error details."""
        errors = [{"resource": "user", "reason": "Already exists"}]
        exc = ConflictException(
            message="Resource conflict",
            errors=errors,
        )

        assert exc.errors == errors


class TestUnprocessableEntityException:
    """Test cases for UnprocessableEntityException."""

    def test_unprocessable_entity_exception_default_status_code(self):
        """Test that UnprocessableEntityException has correct default status code."""
        exc = UnprocessableEntityException(message="Cannot process entity")

        assert exc.status_code == 422
        assert exc.process == "Data Validation"

    def test_unprocessable_entity_exception_with_errors(self):
        """Test UnprocessableEntityException with error details."""
        errors = [{"field": "email", "message": "Invalid format"}]
        exc = UnprocessableEntityException(
            message="Cannot process entity",
            errors=errors,
        )

        assert exc.errors == errors


class TestInternalServerErrorException:
    """Test cases for InternalServerErrorException."""

    def test_internal_server_error_exception_default_status_code(self):
        """Test that InternalServerErrorException has correct default status code."""
        exc = InternalServerErrorException(message="Internal error")

        assert exc.status_code == 500
        assert exc.process == "Internal Server Error"

    def test_internal_server_error_exception_with_errors(self):
        """Test InternalServerErrorException with error details."""
        errors = [{"error": "Database connection failed"}]
        exc = InternalServerErrorException(
            message="Internal error",
            errors=errors,
        )

        assert exc.errors == errors


class TestServiceUnavailableException:
    """Test cases for ServiceUnavailableException."""

    def test_service_unavailable_exception_default_status_code(self):
        """Test that ServiceUnavailableException has correct default status code."""
        exc = ServiceUnavailableException(message="Service unavailable")

        assert exc.status_code == 503
        assert exc.process == "Service Availability"

    def test_service_unavailable_exception_with_errors(self):
        """Test ServiceUnavailableException with error details."""
        errors = [{"service": "database", "status": "down"}]
        exc = ServiceUnavailableException(
            message="Service unavailable",
            errors=errors,
        )

        assert exc.errors == errors


class TestValidationException:
    """Test cases for ValidationException."""

    def test_validation_exception_default_status_code(self):
        """Test that ValidationException has correct default status code."""
        exc = ValidationException(
            message="Validation failed",
            process="validation",
        )

        assert exc.status_code == 422

    def test_validation_exception_custom_status_code(self):
        """Test ValidationException with custom status code."""
        exc = ValidationException(
            message="Validation failed",
            process="validation",
            status_code=400,
        )

        assert exc.status_code == 400

    def test_validation_exception_with_errors(self):
        """Test ValidationException with validation error details."""
        errors = [
            {"field": "email", "message": "Invalid format"},
            {"field": "password", "message": "Too short"},
        ]
        exc = ValidationException(
            message="Validation failed",
            process="validation",
            errors=errors,
        )

        assert exc.errors == errors
        assert len(exc.errors) == 2


class TestBusinessException:
    """Test cases for BusinessException."""

    def test_business_exception_default_status_code(self):
        """Test that BusinessException has correct default status code."""
        exc = BusinessException(
            message="Business rule violation",
            process="business_logic",
        )

        assert exc.status_code == 400

    def test_business_exception_custom_status_code(self):
        """Test BusinessException with custom status code."""
        exc = BusinessException(
            message="Business rule violation",
            process="business_logic",
            status_code=409,
        )

        assert exc.status_code == 409

    def test_business_exception_with_errors(self):
        """Test BusinessException with error details."""
        errors = [{"rule": "balance_check", "message": "Insufficient balance"}]
        exc = BusinessException(
            message="Business rule violation",
            process="business_logic",
            errors=errors,
        )

        assert exc.errors == errors


class TestExceptionInheritance:
    """Test exception inheritance and polymorphism."""

    def test_all_exceptions_inherit_from_business_exception(self):
        """Test that all exceptions inherit from BusinessException."""
        exceptions = [
            BadRequestException("test"),
            UnauthorizedException("test"),
            ForbiddenException("test"),
            NotFoundException("test"),
            ConflictException("test"),
            UnprocessableEntityException("test"),
            InternalServerErrorException("test"),
            ServiceUnavailableException("test"),
            ValidationException("test", "process"),
            BusinessException("test", "process"),
        ]

        for exc in exceptions:
            assert isinstance(exc, BusinessException)
            assert isinstance(exc, Exception)

    def test_all_exceptions_have_to_dict_method(self):
        """Test that all exceptions have to_dict method."""
        exceptions = [
            BadRequestException("test"),
            UnauthorizedException("test"),
            NotFoundException("test"),
            ValidationException("test", "process"),
        ]

        for exc in exceptions:
            result = exc.to_dict()
            assert isinstance(result, dict)
            assert "message" in result
            assert "process" in result
            assert "errors" in result

