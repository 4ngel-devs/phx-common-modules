"""Tests for HTTP exception handlers."""

import pytest
from fastapi import FastAPI, HTTPException, Request
from fastapi.testclient import TestClient
from jose import ExpiredSignatureError

from sucrim.http.errors import (
    BadRequestException,
    BusinessException,
    InternalServerErrorException,
    NotFoundException,
    UnauthorizedException,
)
from sucrim.http.exception_handlers import setup_exception_handlers


class TestExceptionHandlers:
    """Test cases for exception handlers."""

    @pytest.fixture
    def app(self):
        """Create a FastAPI app with exception handlers."""
        app = FastAPI()
        setup_exception_handlers(app)
        return app

    @pytest.fixture
    def client(self, app):
        """Create a test client."""
        return TestClient(app, raise_server_exceptions=False)

    def test_business_exception_handler(self, app, client):
        """Test handler for BusinessException."""

        @app.get("/test-base-exception")
        async def test_endpoint():
            raise BadRequestException(
                message="Invalid request",
                process="test_process",
                errors=[{"field": "id", "message": "Invalid format"}],
            )

        response = client.get("/test-base-exception")

        assert response.status_code == 400
        data = response.json()
        assert data["message"] == "Invalid request"
        assert data["process"] == "test_process"
        assert data["errors"] == [{"field": "id", "message": "Invalid format"}]

    def test_not_found_exception_handler(self, app, client):
        """Test handler for NotFoundException."""

        @app.get("/test-not-found")
        async def test_endpoint():
            raise NotFoundException(
                message="Resource not found",
                process="resource_lookup",
            )

        response = client.get("/test-not-found")

        assert response.status_code == 404
        data = response.json()
        assert data["message"] == "Resource not found"
        assert data["process"] == "resource_lookup"
        assert data["errors"] == []

    def test_unauthorized_exception_handler(self, app, client):
        """Test handler for UnauthorizedException."""

        @app.get("/test-unauthorized")
        async def test_endpoint():
            raise UnauthorizedException(message="Not authenticated")

        response = client.get("/test-unauthorized")

        assert response.status_code == 401
        data = response.json()
        assert data["message"] == "Not authenticated"
        assert data["process"] == "Authentication"

    def test_internal_server_error_exception_handler(self, app, client):
        """Test handler for InternalServerErrorException."""

        @app.get("/test-internal-error")
        async def test_endpoint():
            raise InternalServerErrorException(
                message="Internal server error",
                process="database_operation",
            )

        response = client.get("/test-internal-error")

        assert response.status_code == 500
        data = response.json()
        assert data["message"] == "Internal server error"
        assert data["process"] == "database_operation"

    def test_expired_token_handler(self, app, client):
        """Test handler for ExpiredSignatureError."""

        @app.get("/test-expired-token")
        async def test_endpoint():
            raise ExpiredSignatureError("Token has expired")

        response = client.get("/test-expired-token")

        assert response.status_code == 401
        data = response.json()
        assert data["message"] == "Token has expired."
        assert data["process"] == "access_token"
        assert data["errors"] is None

    def test_http_exception_handler(self, app, client):
        """Test handler for FastAPI HTTPException."""

        @app.get("/test-http-exception")
        async def test_endpoint():
            raise HTTPException(status_code=400, detail="Bad request")

        response = client.get("/test-http-exception")

        assert response.status_code == 400
        data = response.json()
        assert data["message"] == "Bad request"
        assert data["process"] == "general_error"
        assert data["errors"] is None

    def test_http_exception_forbidden_with_specific_message(self, app, client):
        """Test handler for HTTPException 403 with specific message."""

        @app.get("/test-forbidden-specific")
        async def test_endpoint():
            raise HTTPException(
                status_code=403,
                detail="User is required to perform this action",
            )

        response = client.get("/test-forbidden-specific")

        assert response.status_code == 403
        data = response.json()
        assert data["message"] == "You are not authorized to perform this action"
        assert data["process"] == "general_error"

    def test_generic_exception_handler(self, app, client):
        """Test handler for generic exceptions."""

        @app.get("/test-generic-exception")
        async def test_endpoint():
            raise ValueError("Unexpected error")

        response = client.get("/test-generic-exception")

        assert response.status_code == 500
        data = response.json()
        assert data["message"] == "An unexpected error occurred"
        assert data["process"] == "internal_error"
        assert data["errors"] is None

    def test_exception_handler_with_empty_errors(self, app, client):
        """Test exception handler with empty errors list."""

        @app.get("/test-empty-errors")
        async def test_endpoint():
            raise BadRequestException(
                message="Test error",
                errors=[],
            )

        response = client.get("/test-empty-errors")

        assert response.status_code == 400
        data = response.json()
        assert data["errors"] == []

    def test_exception_handler_with_none_errors(self, app, client):
        """Test exception handler with None errors."""

        @app.get("/test-none-errors")
        async def test_endpoint():
            exc = BadRequestException(message="Test error")
            exc.errors = None
            raise exc

        response = client.get("/test-none-errors")

        assert response.status_code == 400
        data = response.json()
        # When errors is None, it should be converted to empty list or None
        # Based on the handler implementation, it should be None
        assert data["errors"] is None or data["errors"] == []

    def test_multiple_exception_types(self, app, client):
        """Test that different exception types are handled correctly."""

        @app.get("/test-400")
        async def test_400():
            raise BadRequestException(message="Bad request")

        @app.get("/test-404")
        async def test_404():
            raise NotFoundException(message="Not found")

        @app.get("/test-500")
        async def test_500():
            raise InternalServerErrorException(message="Internal error")

        response_400 = client.get("/test-400")
        response_404 = client.get("/test-404")
        response_500 = client.get("/test-500")

        assert response_400.status_code == 400
        assert response_404.status_code == 404
        assert response_500.status_code == 500

        assert response_400.json()["message"] == "Bad request"
        assert response_404.json()["message"] == "Not found"
        assert response_500.json()["message"] == "Internal error"

