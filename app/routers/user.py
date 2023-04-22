from app import model
from ..database import SessionLocal, engine, get_db
from ..schemas import  UserCreate, UserResponse
from fastapi import Depends, FastAPI, Response, status, HTTPException,APIRouter
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from ..util import Hash


router=APIRouter(
    prefix="/users",
    tags=["User"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(userpayload: UserCreate, db: Session = Depends(get_db)):
    # Hash the password
    hashed_password=Hash(userpayload.password)
    userpayload.password=hashed_password
    new_user = model.User(**userpayload.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}",response_model=UserResponse)
def get_specific_post(id: int, db: Session = Depends(get_db)):
    get_user = db.query(model.User).filter(model.User.id == id).first()
    if not get_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} is not found")
    return get_user
