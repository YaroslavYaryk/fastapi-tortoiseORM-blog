from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .services import jwt_handler

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return jwt_handler.decodeJWT(data, credentials_exception)
