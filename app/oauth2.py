from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import get_db
from . import schemas,model
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import setting

#  as we are using post /login in auth.py
ouath2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = int(setting.access_token_expiry)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credential_exceptional):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")
        if id is None:
            raise credential_exceptional
        tokken_data = schemas.TokenData(id=id)
    except JWTError:
        raise credential_exceptional
    
    return tokken_data


def get_current_user(token: str = Depends(ouath2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not get current user",
                                         headers={"WWW-Authenticate": "Bearer"})

    token_id= verify_token(token, credential_exception)

    user=db.query(model.User).filter(model.User.id == token_id.id).first()

    return user
