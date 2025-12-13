"""API Response DTO for standardized API responses."""

from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel

from src.data.pagination import Pagination

T = TypeVar("T")


class ApiResponseDto(BaseModel, Generic[T]):
    """Generic API response DTO with optional pagination."""

    data: Optional[T] = None
    pagination: Optional[Pagination] = None

    @classmethod
    def ok(cls, data: Optional[T] = None) -> "ApiResponseDto[T]":
        """
        Create a successful response with data.

        Args:
            data: The response data (optional)

        Returns:
            ApiResponseDto instance with the provided data
        """
        return cls(data=data)

    @classmethod
    def ok_with_pagination(
        cls,
        data: List[T],
        pagination: Pagination,
    ) -> "ApiResponseDto[List[T]]":
        """
        Create a successful paginated response.

        Args:
            data: List of items for the current page
            pagination: Pagination object (total_elements will be set if not already)

        Returns:
            ApiResponseDto instance with data and pagination
        """
        return cls(data=data, pagination=pagination)

    @classmethod
    def ok_from_page(
        cls,
        page_result: List[T],
        pagination: Pagination,
        total_elements: Optional[int] = None,
    ) -> "ApiResponseDto[List[T]]":
        """
        Create a successful paginated response from a page result.

        This method sets total_elements on the pagination object if provided.

        Args:
            page_result: List of items from the page
            pagination: Pagination object
            total_elements: Total number of elements (will be set on pagination)

        Returns:
            ApiResponseDto instance with data and pagination
        """
        if total_elements is not None:
            pagination.total_elements = total_elements
            # Calculate total_pages if we have size
            if pagination.size > 0:
                pagination.total_pages = (total_elements + pagination.size - 1) // pagination.size

        return cls(data=page_result, pagination=pagination)
