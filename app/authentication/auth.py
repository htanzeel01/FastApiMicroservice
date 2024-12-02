from typing import List, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from app.config import config  # Ensure this imports correctly

# Configuration from config.py
JWT_SECRET_KEY = config.jwt_key  # "devKey development"
JWT_ALGORITHM = "HS256"
JWT_ISSUER = config.jwt_issuer  # "DrinkAppRecipes.azurewebsites.net"
JWT_AUDIENCE = config.jwt_audience  # Set as a string

# Define a model for the JWT payload
class TokenData(BaseModel):
    sub: Optional[str] = None
    roles: List[str] = []
    phone_number: Optional[str] = None

# Initialize the HTTPBearer security scheme
security = HTTPBearer()

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """Decodes and validates a JWT token."""
    token = credentials.credentials
    try:
        # Decode JWT
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            issuer=JWT_ISSUER,
            audience=JWT_AUDIENCE
        )

        # Extract fields from the payload
        sub: str = payload.get("http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier")
        roles = payload.get("http://schemas.microsoft.com/ws/2008/06/identity/claims/role")

        # Normalize roles to always be a list
        if isinstance(roles, str):
            roles = [roles]  # Convert single role string to a list
        elif roles is None:
            roles = []  # Default to empty list if no roles are provided

        # Debugging output
        print(f"Token subject (phone number): {sub}, roles: {roles}")

        # Ensure the subject exists
        if sub is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing phone number",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return TokenData(sub=sub, roles=roles, phone_number=sub)

    except JWTError as e:
        print(f"JWT Error: {str(e)}")  # Debugging output
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_roles(required_roles: List[str]):
    """
    Dependency that checks whether the authenticated user has at least one of the required roles.
    """
    def role_checker(token_data: TokenData = Depends(verify_jwt_token)):
        print("User roles:", token_data.roles)  # Debugging output
        print("Required roles:", required_roles)  # Debugging output

        user_roles = token_data.roles
        # Check if any required role is present in the user's roles
        if not any(role.upper() in (ur.upper() for ur in user_roles) for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return token_data

    return role_checker
