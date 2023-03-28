"""
Auth0 helper module
"""
import json
from urllib.request import urlopen

from fastapi import Request, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from app.config.auth import set_up
from app.utils.exceptions import AuthError

auth0_settings = set_up()


def get_token_auth_header(credentials: HTTPAuthorizationCredentials) -> str:
    """Obtains the Access Token from the Authorization Header"""
    if not credentials:
        raise AuthError(
            {
                "code": "authorization_header_missing",
                "description": "Authorization header is expected",
            },
            status.HTTP_401_UNAUTHORIZED,
        )

    if credentials.scheme.lower() != "bearer":
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must start with" " Bearer",
            },
            status.HTTP_401_UNAUTHORIZED,
        )

    token = credentials.credentials
    return token


def validate_token(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
):
    """
    Auth0 token validation
    """
    token = get_token_auth_header(credentials)
    jwks = get_jwks()
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    if rsa_key:
        try:
            jwt_decoded = jwt.decode(
                token,
                rsa_key,
                algorithms=auth0_settings["ALGORITHMS"],
                audience=auth0_settings["API_AUDIENCE"],
                issuer=f"https://{auth0_settings['DOMAIN']}/",
            )
        except jwt.ExpiredSignatureError:
            raise AuthError(
                {"code": "token_expired", "description": "token is expired"},
                status.HTTP_401_UNAUTHORIZED,
            )
        except jwt.JWTClaimsError:
            raise AuthError(
                {
                    "code": "invalid_claims",
                    "description": "incorrect claims,"
                    "please check the audience and issuer",
                },
                status.HTTP_401_UNAUTHORIZED,
            )
        except Exception:
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": "Unable to parse authentication" " token.",
                },
                status.HTTP_401_UNAUTHORIZED,
            )

        set_auth0_client_id(request, jwt_decoded.get("azp", None))

        return None
    raise AuthError(
        {
            "code": "invalid_header",
            "description": "Unable to find appropriate key",
        },
        status.HTTP_401_UNAUTHORIZED,
    )


def get_jwks() -> dict:
    """Get jwks from auth0

    Returns:
        dict: jwks
    """
    json_url = urlopen(f"https://{auth0_settings['DOMAIN']}/.well-known/jwks.json")
    jwks = json.loads(json_url.read())
    return jwks


def set_auth0_client_id(request: Request, client_id: str):
    request.state.client_id = client_id
