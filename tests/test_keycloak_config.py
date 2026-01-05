"""Tests for Keycloak configuration module."""

import os
from unittest.mock import patch

import pytest

from sucrim.keycloak.keycloak_config import (
    KeycloakConfig,
    get_idp,
    get_keycloak_config,
)


class TestKeycloakConfig:
    """Test cases for KeycloakConfig."""

    def test_keycloak_config_initialization_with_env_vars(self):
        """Test that KeycloakConfig reads from environment variables."""
        with patch.dict(
            os.environ,
            {
                "KC_SERVER_URL": "https://keycloak.example.com",
                "KC_CLIENT_ID": "test-client",
                "KC_CLIENT_SECRET": "test-secret",
                "KC_ADMIN_CLIENT_ID": "admin-client",
                "KC_ADMIN_CLIENT_SECRET": "admin-secret",
                "KC_REALM": "test-realm",
                "KC_CALLBACK_URI": "https://app.example.com/callback",
            },
        ):
            config = KeycloakConfig()

            assert config.server_url == "https://keycloak.example.com"
            assert config.client_id == "test-client"
            assert config.client_secret == "test-secret"
            assert config.admin_client_id == "admin-client"
            assert config.admin_client_secret == "admin-secret"
            assert config.realm == "test-realm"
            assert config.callback_uri == "https://app.example.com/callback"

    def test_keycloak_config_initialization_without_env_vars(self):
        """Test that KeycloakConfig returns None when env vars are not set."""
        with patch.dict(os.environ, {}, clear=True):
            config = KeycloakConfig()

            assert config.server_url is None
            assert config.client_id is None
            assert config.client_secret is None
            assert config.admin_client_id is None
            assert config.admin_client_secret is None
            assert config.realm is None
            assert config.callback_uri is None

    def test_keycloak_config_partial_env_vars(self):
        """Test KeycloakConfig with only some environment variables set."""
        with patch.dict(
            os.environ,
            {
                "KC_SERVER_URL": "https://keycloak.example.com",
                "KC_CLIENT_ID": "test-client",
                "KC_REALM": "test-realm",
            },
        ):
            config = KeycloakConfig()

            assert config.server_url == "https://keycloak.example.com"
            assert config.client_id == "test-client"
            assert config.realm == "test-realm"
            assert config.client_secret is None
            assert config.admin_client_id is None
            assert config.admin_client_secret is None
            assert config.callback_uri is None

    def test_keycloak_config_model_dump(self):
        """Test that KeycloakConfig can be converted to dictionary."""
        with patch.dict(
            os.environ,
            {
                "KC_SERVER_URL": "https://keycloak.example.com",
                "KC_CLIENT_ID": "test-client",
                "KC_REALM": "test-realm",
            },
        ):
            config = KeycloakConfig()
            config_dict = config.model_dump()

            assert isinstance(config_dict, dict)
            assert config_dict["server_url"] == "https://keycloak.example.com"
            assert config_dict["client_id"] == "test-client"
            assert config_dict["realm"] == "test-realm"
            assert config_dict["client_secret"] is None

    def test_keycloak_config_is_pydantic_model(self):
        """Test that KeycloakConfig is a Pydantic BaseModel."""
        from pydantic import BaseModel

        assert issubclass(KeycloakConfig, BaseModel)


class TestGetKeycloakConfig:
    """Test cases for get_keycloak_config function."""

    def test_get_keycloak_config_returns_singleton(self):
        """Test that get_keycloak_config returns the same instance (singleton)."""
        # Reset the global variable by importing and clearing
        import sucrim.keycloak.keycloak_config as kc_module

        kc_module._keycloak_config = None

        config1 = get_keycloak_config()
        config2 = get_keycloak_config()

        assert config1 is config2
        assert id(config1) == id(config2)

    def test_get_keycloak_config_creates_new_instance_if_none(self):
        """Test that get_keycloak_config creates a new instance if None."""
        import sucrim.keycloak.keycloak_config as kc_module

        kc_module._keycloak_config = None

        config = get_keycloak_config()

        assert config is not None
        assert isinstance(config, KeycloakConfig)

    def test_get_keycloak_config_reads_env_vars(self):
        """Test that get_keycloak_config reads environment variables."""
        import sucrim.keycloak.keycloak_config as kc_module

        kc_module._keycloak_config = None

        with patch.dict(
            os.environ,
            {
                "KC_SERVER_URL": "https://keycloak.example.com",
                "KC_CLIENT_ID": "test-client",
                "KC_REALM": "test-realm",
            },
        ):
            config = get_keycloak_config()

            assert config.server_url == "https://keycloak.example.com"
            assert config.client_id == "test-client"
            assert config.realm == "test-realm"


class TestGetIdp:
    """Test cases for get_idp function."""

    @patch("sucrim.keycloak.keycloak_config.FastAPIKeycloak")
    def test_get_idp_returns_singleton(self, mock_fastapi_keycloak):
        """Test that get_idp returns the same instance (singleton)."""
        import sucrim.keycloak.keycloak_config as kc_module

        kc_module._idp_instance = None
        kc_module._keycloak_config = None

        # Mock the FastAPIKeycloak instance
        mock_instance = mock_fastapi_keycloak.return_value

        idp1 = get_idp()
        idp2 = get_idp()

        assert idp1 is idp2
        assert id(idp1) == id(idp2)

    @patch("sucrim.keycloak.keycloak_config.FastAPIKeycloak")
    def test_get_idp_creates_new_instance_if_none(self, mock_fastapi_keycloak):
        """Test that get_idp creates a new instance if None."""
        import sucrim.keycloak.keycloak_config as kc_module

        kc_module._idp_instance = None
        kc_module._keycloak_config = None

        mock_instance = mock_fastapi_keycloak.return_value

        idp = get_idp()

        assert idp is not None
        assert idp == mock_instance

    @patch("sucrim.keycloak.keycloak_config.FastAPIKeycloak")
    @patch("sucrim.keycloak.keycloak_config.get_keycloak_config")
    def test_get_idp_uses_config_from_get_keycloak_config(
        self, mock_get_config, mock_fastapi_keycloak
    ):
        """Test that get_idp uses configuration from get_keycloak_config."""
        import sucrim.keycloak.keycloak_config as kc_module

        kc_module._idp_instance = None

        # Mock the config
        mock_config = KeycloakConfig(
            server_url="https://keycloak.example.com",
            client_id="test-client",
            client_secret="test-secret",
            admin_client_id="admin-client",
            admin_client_secret="admin-secret",
            realm="test-realm",
            callback_uri="https://app.example.com/callback",
        )
        mock_get_config.return_value = mock_config

        get_idp()

        # Verify FastAPIKeycloak was called with config.model_dump()
        mock_fastapi_keycloak.assert_called_once()
        call_args = mock_fastapi_keycloak.call_args[1]  # Get keyword arguments

        assert call_args["server_url"] == "https://keycloak.example.com"
        assert call_args["client_id"] == "test-client"
        assert call_args["client_secret"] == "test-secret"
        assert call_args["admin_client_id"] == "admin-client"
        assert call_args["admin_client_secret"] == "admin-secret"
        assert call_args["realm"] == "test-realm"
        assert call_args["callback_uri"] == "https://app.example.com/callback"

    @patch("sucrim.keycloak.keycloak_config.FastAPIKeycloak")
    def test_get_idp_calls_fastapi_keycloak_with_config(self, mock_fastapi_keycloak):
        """Test that get_idp calls FastAPIKeycloak with correct parameters."""
        import sucrim.keycloak.keycloak_config as kc_module

        kc_module._idp_instance = None
        kc_module._keycloak_config = None

        with patch.dict(
            os.environ,
            {
                "KC_SERVER_URL": "https://keycloak.example.com",
                "KC_CLIENT_ID": "test-client",
                "KC_CLIENT_SECRET": "test-secret",
                "KC_ADMIN_CLIENT_ID": "admin-client",
                "KC_ADMIN_CLIENT_SECRET": "admin-secret",
                "KC_REALM": "test-realm",
                "KC_CALLBACK_URI": "https://app.example.com/callback",
            },
        ):
            get_idp()

            # Verify FastAPIKeycloak was called
            mock_fastapi_keycloak.assert_called_once()
            call_kwargs = mock_fastapi_keycloak.call_args[1]

            assert call_kwargs["server_url"] == "https://keycloak.example.com"
            assert call_kwargs["client_id"] == "test-client"
            assert call_kwargs["client_secret"] == "test-secret"
            assert call_kwargs["admin_client_id"] == "admin-client"
            assert call_kwargs["admin_client_secret"] == "admin-secret"
            assert call_kwargs["realm"] == "test-realm"
            assert call_kwargs["callback_uri"] == "https://app.example.com/callback"

