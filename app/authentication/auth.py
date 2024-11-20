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

        # Extract subject (phone number) and role from the payload
        sub: str = payload.get("http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier")
        role: str = payload.get("http://schemas.microsoft.com/ws/2008/06/identity/claims/role")

        # Debugging information
        print(f"Token subject (phone number): {sub}, roles: {role}")

        # Check if subject (phone number) and role are present
        if sub is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing phone number",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing role",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Convert role to a list
        user_roles = [role]  # Make it a list to match TokenData's expected format

        return TokenData(sub=sub, roles=user_roles, phone_number=sub)
    except JWTError as e:
        print(f"JWT Error: {str(e)}")  # Debugging information
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_roles(required_roles: List[str]):
    def role_checker(token_data: TokenData = Depends(verify_jwt_token)):
        print("User roles:", token_data.roles)  # Debug statement
        print("Required roles:", required_roles)  # Debug statement
        user_roles = token_data.roles
        if not any(role.upper() in [ur.upper() for ur in user_roles] for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return token_data

    return role_checker
