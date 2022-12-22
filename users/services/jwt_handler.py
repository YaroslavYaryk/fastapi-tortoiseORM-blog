import time
from typing import Dict
from datetime import datetime, timedelta

from jose import jwt
from decouple import config

JWT_SECRET = config("SECRET_KEY")
JWT_ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config("ACCESS_TOKEN_EXPIRE_MINUTES"))

# returns gererated token
def token_response(token: str):
    return {"access_token": token}


# function used for signing the JWT string
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = time.time() + ACCESS_TOKEN_EXPIRE_MINUTES * 60
    to_encode.update({"expires": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def decodeJWT(token: str, credentials_exception):

    try:
        decoded_token = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
        if decoded_token["expires"] < time.time():
            raise credentials_exception
        if not decoded_token.get("user_data"):
            raise credentials_exception
        else:
            return decoded_token["user_data"]
    except Exception as ex:
        print(ex)
        raise credentials_exception
