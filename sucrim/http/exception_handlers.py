"""Exception handlers for FastAPI applications."""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from jose import ExpiredSignatureError

from sucrim.http.errors import BusinessException


def setup_exception_handlers(app: FastAPI) -> None:
    """
    Setup standard exception handlers for FastAPI application.
    
    This function registers handlers for:
    - BusinessException (custom exceptions - base for all custom exceptions)
    - ExpiredSignatureError (expired JWT tokens)
    - HTTPException (FastAPI HTTP exceptions)
    - Exception (generic catch-all)
    
    Args:
        app: FastAPI application instance
    """
    @app.exception_handler(BusinessException)
    async def business_exception_handler(request: Request, exc: BusinessException):
        """Handle custom business exceptions."""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": exc.message,
                "process": exc.process,
                "errors": exc.errors,
            },
        )

    @app.exception_handler(ExpiredSignatureError)
    async def expired_token_handler(request: Request, exc: ExpiredSignatureError):
        """Handle expired JWT tokens."""
        return JSONResponse(
            status_code=401,
            content={
                "message": "Token has expired.",
                "process": "access_token",
                "errors": None,
            },
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle FastAPI HTTP exceptions."""
        # Check for specific unauthorized messages
        if exc.status_code == 403 and "is required to perform this action" in str(exc.detail):
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "message": "You are not authorized to perform this action",
                    "process": "general_error",
                    "errors": None,
                },
            )
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": str(exc.detail),
                "process": "general_error",
                "errors": None,
            },
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        """Handle unexpected exceptions."""
        return JSONResponse(
            status_code=500,
            content={
                "message": "An unexpected error occurred",
                "process": "internal_error",
                "errors": None,
            },
        )

