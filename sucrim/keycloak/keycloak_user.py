"""Keycloak user model for representing authenticated users."""

from typing import List, Optional

from pydantic import BaseModel, Field


class KeycloakUser(BaseModel):
    """
    Keycloak user model.
    
    Represents an authenticated user from Keycloak with all relevant information.
    """

    username: Optional[str] = Field(
        default=None,
        description="Username of the authenticated user"
    )
    keycloak_user_id: Optional[str] = Field(
        default=None,
        description="Keycloak user ID (UUID)"
    )
    tenant_id: Optional[str] = Field(
        default=None,
        description="Tenant ID for multi-tenant applications"
    )
    email: Optional[str] = Field(
        default=None,
        description="User email address"
    )
    first_name: Optional[str] = Field(
        default=None,
        description="User first name"
    )
    last_name: Optional[str] = Field(
        default=None,
        description="User last name"
    )
    realm: Optional[str] = Field(
        default=None,
        description="Keycloak realm name"
    )
    client_id: Optional[str] = Field(
        default=None,
        description="Keycloak client ID"
    )
    roles: List[str] = Field(
        default_factory=list,
        description="List of user roles"
    )
    email_verified: Optional[bool] = Field(
        default=None,
        description="Whether the user's email is verified"
    )

    class Config:
        """Pydantic configuration."""

        from_attributes = True

