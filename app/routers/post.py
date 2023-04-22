from typing import List, Optional
from app import model
from ..database import get_db
from ..schemas import PostCreate, PostUpdate, PostResponse, PostVote
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Post"]
)

# @router.get("/sql")
# def root(db: Session = Depends(get_db)):
#     all_post = db.query(model.Post).all()
#     return all_post


@router.get("/", response_model=List[PostVote])
def get_post(db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0,
             search: Optional[str] = ""):
    # print(current_user.id)
    # all_post = db.query(model.Post).filter(
    #     model.Post.title.contains(search)).limit(limit).offset(skip).all()  # type: ignore
    # label is as in sql
    results = db.query(model.Post, func.count(model.Vote.post_id).label("votes")).join(
        model.Vote, model.Post.id == model.Vote.post_id, isouter=True).group_by(model.Post.id).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()  # type: ignore

    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(payload: PostCreate, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    #    new_post=model.Post(title=payload.title,content=payload.content,published=payload.published)
    new_post = model.Post(user_id=current_user.id, **payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=PostVote)
def get_specific_post(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    # fetch_post = db.query(model.Post).filter(model.Post.id == id).first()
    fetch_post = db.query(model.Post, func.count(model.Vote.post_id).label("votes")).join(
        model.Vote, model.Post.id == model.Vote.post_id, isouter=True).group_by(model.Post.id).filter(model.Post.id == id).first()
    if not fetch_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} is not found")
    if fetch_post.Post.user_id != current_user.id:  # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to acess this post")

    return fetch_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_specific_post(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    delete_post = db.query(model.Post).filter(model.Post.id == id)
    if not delete_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} is not found")

    if delete_post.first().user_id != current_user.id:  # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to delete this post")

    delete_post.delete(synchronize_session=False)
    db.commit()


@router.put("/{id}", response_model=PostResponse)
def update_specific_post(id: int, payload: PostUpdate, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    update_post = db.query(model.Post).filter(model.Post.id == id)
    if not update_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} is not found")
    if update_post.first().user_id != current_user.id:  # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to delete this post")

    update_post.update(payload.dict(), synchronize_session=False)
    db.commit()
    return update_post.first()
