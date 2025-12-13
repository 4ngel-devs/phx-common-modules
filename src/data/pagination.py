"""Pagination data model."""

from typing import Optional

from pydantic import BaseModel, Field


class Pagination(BaseModel):
    """Pagination information for paginated responses."""

    page: int = Field(default=0, ge=0, description="Page number (0-indexed)")
    size: int = Field(default=10, gt=0, description="Page size")
    total_elements: Optional[int] = Field(default=None, ge=0, description="Total number of elements")
    total_pages: Optional[int] = Field(default=None, ge=0, description="Total number of pages")

    class Config:
        """Pydantic configuration."""

        frozen = False  # Allow mutation for setting total_elements

