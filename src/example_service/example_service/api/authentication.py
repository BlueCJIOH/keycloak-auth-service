import os
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from keycloak import KeycloakOpenID


class KeycloakAuthentication(BaseAuthentication):
    """Authenticate requests using Keycloak-issued JWT tokens."""

    def __init__(self):
        server_url = os.environ.get(
            "KEYCLOAK_SERVER_URL",
            "http://localhost:8080/",
        )
        realm_name = os.environ.get("KEYCLOAK_REALM", "demo")
        client_id = os.environ.get("KEYCLOAK_CLIENT_ID", "demo-client")
        client_secret = os.environ.get("KEYCLOAK_CLIENT_SECRET", "")
        self.keycloak_openid = KeycloakOpenID(
            server_url=server_url,
            realm_name=realm_name,
            client_id=client_id,
            client_secret_key=client_secret,
        )
        try:
            self.public_key = (
                "-----BEGIN PUBLIC KEY-----\n"
                + self.keycloak_openid.public_key()
                + "\n-----END PUBLIC KEY-----"
            )
        except Exception:
            self.public_key = None

    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if not auth_header.startswith("Bearer "):
            return None
        token = auth_header.split()[1]
        if not self.public_key:
            raise exceptions.AuthenticationFailed(
                "Keycloak public key not available",
            )
        options = {
            "verify_signature": True,
            "verify_aud": False,
            "verify_exp": True,
        }
        try:
            decoded = self.keycloak_openid.decode_token(
                token, key=self.public_key, options=options
            )
        except Exception as exc:
            raise exceptions.AuthenticationFailed("Invalid token") from exc
        user = type(
            "User", (), {"username": decoded.get("preferred_username", "user")}
        )()
        return (user, token)
