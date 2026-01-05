"""Keycloak authentication provider with automatic reconnection."""

import time
from typing import Optional

import httpx
from loguru import logger

from sucrim.keycloak.keycloak_config import KeycloakConfig, get_keycloak_config


class KeycloakAuthProvider:
    """
    Keycloak authentication provider with automatic reconnection.
    
    Manages Keycloak admin client authentication with automatic token refresh
    and reconnection every 15 minutes.
    """

    RECONNECT_INTERVAL_SECONDS = 15 * 60  # 15 minutes
    CONNECTION_TIMEOUT_SECONDS = 10
    BEARER_PREFIX = "Bearer "

    def __init__(self, config: Optional[KeycloakConfig] = None):
        """
        Initialize Keycloak authentication provider.

        Args:
            config: KeycloakConfig instance (if None, uses singleton from get_keycloak_config())
        """
        self.config = config or get_keycloak_config()
        self._access_token: Optional[str] = None
        self._token_expires_at: float = 0.0
        self._last_init_time: float = 0.0
        self._client: Optional[httpx.AsyncClient] = None
        self._initialize()

    def _initialize(self) -> None:
        """Initialize the Keycloak client and get initial token."""
        try:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(
                    self.CONNECTION_TIMEOUT_SECONDS,
                    connect=self.CONNECTION_TIMEOUT_SECONDS,
                ),
                limits=httpx.Limits(max_connections=50, max_keepalive_connections=20),
            )
            self._last_init_time = time.time()
            self._refresh_token()
            logger.info(
                f"Keycloak client initialized successfully for realm: {self.config.realm}"
            )
        except Exception as e:
            logger.error(
                f"Failed to initialize Keycloak client: {type(e).__name__} - {str(e)}",
                exc_info=True,
            )
            raise RuntimeError(
                f"Failed to initialize Keycloak authentication provider: {str(e)}"
            ) from e

    def _refresh_token(self) -> str:
        """
        Refresh the admin access token.

        Returns:
            Access token string
        """
        if not self.config.server_url or not self.config.realm:
            raise ValueError("Keycloak server URL and realm must be configured")

        token_url = (
            f"{self.config.server_url}/realms/{self.config.realm}/protocol/openid-connect/token"
        )

        data = {
            "grant_type": "client_credentials",
            "client_id": self.config.admin_client_id or self.config.client_id,
            "client_secret": self.config.admin_client_secret or self.config.client_secret,
        }

        try:
            # Use sync client for token refresh
            with httpx.Client(timeout=self.CONNECTION_TIMEOUT_SECONDS) as client:
                response = client.post(token_url, data=data)
                response.raise_for_status()
                token_data = response.json()

            self._access_token = token_data.get("access_token")
            expires_in = token_data.get("expires_in", 300)  # Default 5 minutes
            self._token_expires_at = time.time() + expires_in - 60  # Refresh 1 min early

            if not self._access_token:
                raise ValueError("Access token not found in response")

            logger.debug("Keycloak admin access token refreshed successfully")
            return self._access_token

        except httpx.HTTPError as e:
            logger.error(f"Failed to refresh Keycloak token: {str(e)}", exc_info=True)
            raise RuntimeError(f"Failed to refresh Keycloak token: {str(e)}") from e

    def _ensure_initialized(self) -> None:
        """Ensure the client is initialized."""
        if self._client is None:
            raise RuntimeError(
                "Keycloak client has not been initialized. Call _initialize() first."
            )

    def _reconnect_if_needed(self) -> None:
        """Reconnect if the reconnect interval has passed."""
        current_time = time.time()
        if current_time - self._last_init_time > self.RECONNECT_INTERVAL_SECONDS:
            logger.info(
                f"Reconnecting Keycloak client after {self.RECONNECT_INTERVAL_SECONDS / 60} minutes"
            )
            self._initialize()

    def get_admin_access_token(self) -> str:
        """
        Get admin access token, refreshing if needed.

        Returns:
            Access token string
        """
        self._ensure_initialized()
        self._reconnect_if_needed()

        # Refresh token if expired or about to expire
        if time.time() >= self._token_expires_at:
            self._refresh_token()

        if not self._access_token:
            self._refresh_token()

        return self._access_token

    def get_admin_access_token_string(self) -> str:
        """
        Get admin access token with Bearer prefix.

        Returns:
            Access token string with "Bearer " prefix
        """
        token = self.get_admin_access_token()
        return f"{self.BEARER_PREFIX}{token}"

    async def get_client(self) -> httpx.AsyncClient:
        """
        Get the HTTP client instance.

        Returns:
            httpx.AsyncClient instance
        """
        self._ensure_initialized()
        self._reconnect_if_needed()
        return self._client

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None

