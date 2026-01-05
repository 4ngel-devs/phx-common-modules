"""Keycloak JWT token decoder for extracting user information."""

from typing import List, Optional

from jose import jwt
from jose.exceptions import JWTError
from loguru import logger

from sucrim.http.errors import UnauthorizedException
from sucrim.keycloak.keycloak_user import KeycloakUser


class KeycloakJwtDecoder:
    """
    Keycloak JWT token decoder.
    
    Decodes JWT tokens from Keycloak and extracts user information
    into a KeycloakUser object.
    """

    BEARER_PREFIX = "Bearer "
    JWT_PARTS_COUNT = 3

    @staticmethod
    def decode_token(token: str) -> Optional[KeycloakUser]:
        """
        Decode a JWT token and extract user information.

        Note: This method decodes the token without signature verification.
        For production use, you should verify the signature using Keycloak's
        public key for security.

        Args:
            token: JWT token string (with or without "Bearer " prefix)

        Returns:
            KeycloakUser object with extracted information, or None if token is invalid

        Raises:
            UnauthorizedException: If token is invalid or cannot be decoded
        """
        if not token or not token.strip():
            logger.error("Token is null or empty")
            raise UnauthorizedException(
                message="Token is null or empty",
                process="token_decode"
            )

        if not KeycloakJwtDecoder._is_valid_jwt_format(token):
            logger.error("Invalid JWT format")
            raise UnauthorizedException(
                message="Invalid JWT format",
                process="token_decode"
            )

        try:
            normalized_token = KeycloakJwtDecoder._normalize_token(token)
            
            # Decode without verification (for extracting claims only)
            # Note: For production, you should verify the signature using Keycloak's public key
            # Using an empty string as key and options={"verify_signature": False} to decode without verification
            claims = jwt.decode(
                normalized_token,
                key="",  # Empty key since we're not verifying
                options={"verify_signature": False}
            )

            user = KeycloakUser(
                username=KeycloakJwtDecoder._get_claim_as_string(claims, "preferred_username"),
                keycloak_user_id=KeycloakJwtDecoder._get_claim_as_string(claims, "sid"),
                tenant_id=KeycloakJwtDecoder._get_claim_as_string(claims, "tenantId"),
                email=KeycloakJwtDecoder._get_claim_as_string(claims, "email"),
                first_name=KeycloakJwtDecoder._get_claim_as_string(claims, "given_name"),
                last_name=KeycloakJwtDecoder._get_claim_as_string(claims, "family_name"),
                realm=KeycloakJwtDecoder._extract_realm(claims),
                client_id=KeycloakJwtDecoder._get_claim_as_string(claims, "azp"),
                roles=KeycloakJwtDecoder._extract_roles(claims),
                email_verified=KeycloakJwtDecoder._get_claim_as_boolean(claims, "email_verified"),
            )

            logger.debug(f"Successfully decoded JWT token for user: {user.username}")
            return user

        except JWTError as e:
            logger.error(f"Failed to decode JWT token: {str(e)}", exc_info=True)
            raise UnauthorizedException(
                message="Failed to decode JWT token",
                process="token_decode"
            ) from e
        except Exception as e:
            logger.error(f"Unexpected error decoding JWT token: {str(e)}", exc_info=True)
            raise UnauthorizedException(
                message="Failed to decode JWT token",
                process="token_decode"
            ) from e

    @staticmethod
    def _normalize_token(token: str) -> str:
        """
        Remove Bearer prefix from token if present.

        Args:
            token: Token string

        Returns:
            Token without Bearer prefix
        """
        if token.startswith(KeycloakJwtDecoder.BEARER_PREFIX):
            return token[len(KeycloakJwtDecoder.BEARER_PREFIX) :]
        return token

    @staticmethod
    def _get_claim_as_string(claims: dict, claim_name: str) -> Optional[str]:
        """
        Get a claim value as string.

        Args:
            claims: JWT claims dictionary
            claim_name: Name of the claim

        Returns:
            Claim value as string, or None if not present
        """
        value = claims.get(claim_name)
        if value is None:
            logger.warning(
                f"Claim '{claim_name}' not found in JWT token. Setting to None."
            )
            return None
        return str(value) if not isinstance(value, str) else value

    @staticmethod
    def _get_claim_as_boolean(claims: dict, claim_name: str) -> Optional[bool]:
        """
        Get a claim value as boolean.

        Args:
            claims: JWT claims dictionary
            claim_name: Name of the claim

        Returns:
            Claim value as boolean, or None if not present
        """
        value = claims.get(claim_name)
        if value is None:
            logger.warning(
                f"Claim '{claim_name}' not found in JWT token. Setting to None."
            )
            return None
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("true", "1", "yes")
        return bool(value)

    @staticmethod
    def _extract_realm(claims: dict) -> Optional[str]:
        """
        Extract realm from JWT claims.

        Tries to extract from issuer (iss) claim first, then from realm claim.

        Args:
            claims: JWT claims dictionary

        Returns:
            Realm name, or None if not found
        """
        # Try to extract from issuer
        issuer = claims.get("iss")
        if issuer and isinstance(issuer, str) and "/realms/" in issuer:
            parts = issuer.split("/realms/")
            if len(parts) > 1:
                realm = parts[1].split("/")[0]
                if realm:
                    return realm

        # Fallback to realm claim
        realm = claims.get("realm")
        if realm is None:
            logger.warning(
                "Realm not found in JWT token (neither in 'iss' nor 'realm' claim). Setting to None."
            )
        return str(realm) if realm is not None else None

    @staticmethod
    def _extract_roles(claims: dict) -> List[str]:
        """
        Extract roles from JWT claims.

        Extracts both realm roles and client roles from resource_access.

        Args:
            claims: JWT claims dictionary

        Returns:
            List of role names
        """
        roles: List[str] = []

        # Extract realm roles
        realm_access = claims.get("realm_access")
        if realm_access is None:
            logger.warning(
                "Claim 'realm_access' not found in JWT token. No realm roles will be extracted."
            )
        elif isinstance(realm_access, dict):
            realm_roles = realm_access.get("roles")
            if realm_roles is None:
                logger.warning(
                    "Field 'roles' not found in 'realm_access' claim. No realm roles will be extracted."
                )
            elif isinstance(realm_roles, list):
                roles.extend([str(role) for role in realm_roles if role])

        # Extract client roles (from resource_access)
        resource_access = claims.get("resource_access")
        if resource_access is None:
            logger.warning(
                "Claim 'resource_access' not found in JWT token. No client roles will be extracted."
            )
        elif isinstance(resource_access, dict):
            for client_access in resource_access.values():
                if isinstance(client_access, dict):
                    client_roles = client_access.get("roles")
                    if isinstance(client_roles, list):
                        roles.extend([str(role) for role in client_roles if role])

        if not roles:
            logger.warning(
                "No roles found in JWT token (checked 'realm_access' and 'resource_access'). Returning empty list."
            )

        return roles

    @staticmethod
    def _is_valid_jwt_format(token: str) -> bool:
        """
        Check if token has valid JWT format (3 parts separated by dots).

        Args:
            token: Token string

        Returns:
            True if format is valid, False otherwise
        """
        normalized = KeycloakJwtDecoder._normalize_token(token)
        parts = normalized.split(".")
        return len(parts) == KeycloakJwtDecoder.JWT_PARTS_COUNT

