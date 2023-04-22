from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, model, util, oauth2

router = APIRouter(tags=["Authentication"])


@router.post("/login",response_model=schemas.TokenResponse)
# def login(user_cred: schemas.UserLogin, db: Session = Depends(database.get_db)):
# outh2passwordRequestForm return in format
# {
# "username":"df"
# "password":"asd"
# }
def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(model.User).filter(
        model.User.email == user_cred.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User with email: {user_cred.username} is not found")
    if not util.Verify(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")

    # create a token
    # return token
    # in data you can paas the value which we want if we decode access_token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
