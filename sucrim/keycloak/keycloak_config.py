"""Keycloak configuration for Phoenix microservices."""

from os import environ
from typing import Optional

from fastapi_keycloak import FastAPIKeycloak
from pydantic import BaseModel, Field


class KeycloakConfig(BaseModel):
    """
    Keycloak configuration model.
    
    Reads configuration from environment variables:
    - KC_SERVER_URL: Keycloak server URL
    - KC_CLIENT_ID: Client ID for authentication
    - KC_CLIENT_SECRET: Client secret for authentication
    - KC_ADMIN_CLIENT_ID: Admin client ID
    - KC_ADMIN_CLIENT_SECRET: Admin client secret
    - KC_REALM: Keycloak realm name
    - KC_CALLBACK_URI: OAuth callback URI
    """

    server_url: Optional[str] = Field(default_factory=lambda: environ.get("KC_SERVER_URL", None))
    client_id: Optional[str] = Field(default_factory=lambda: environ.get("KC_CLIENT_ID", None))
    client_secret: Optional[str] = Field(default_factory=lambda: environ.get("KC_CLIENT_SECRET", None))
    admin_client_id: Optional[str] = Field(default_factory=lambda: environ.get("KC_ADMIN_CLIENT_ID", None))
    admin_client_secret: Optional[str] = Field(default_factory=lambda: environ.get("KC_ADMIN_CLIENT_SECRET", None))
    realm: Optional[str] = Field(default_factory=lambda: environ.get("KC_REALM", None))
    callback_uri: Optional[str] = Field(default_factory=lambda: environ.get("KC_CALLBACK_URI", None))


# Global instance (singleton pattern)
_keycloak_config: Optional[KeycloakConfig] = None
_idp_instance: Optional[FastAPIKeycloak] = None


def get_keycloak_config() -> KeycloakConfig:
    """
    Get Keycloak configuration instance (singleton).
    
    Returns:
        KeycloakConfig: Configuration instance
    """
    global _keycloak_config
    if _keycloak_config is None:
        _keycloak_config = KeycloakConfig()
    return _keycloak_config


def get_idp() -> FastAPIKeycloak:
    """
    Get FastAPIKeycloak instance (singleton).
    
    This is the main instance used for authentication in FastAPI apps.
    
    Returns:
        FastAPIKeycloak: FastAPIKeycloak instance configured with Keycloak settings
    """
    global _idp_instance
    if _idp_instance is None:
        config = get_keycloak_config()
        _idp_instance = FastAPIKeycloak(**config.model_dump())
    return _idp_instance

