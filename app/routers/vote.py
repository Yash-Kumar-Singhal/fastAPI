from fastapi import Depends,status, HTTPException,APIRouter
from ..schemas import  Vote
from ..database import get_db
from sqlalchemy.orm import Session
from .. import oauth2
from app import model



router=APIRouter(
    prefix="/vote",
    tags=["vote"]
)



@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(votepayload: Vote, db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):

    fetch_post = db.query(model.Post).filter(model.Post.id == votepayload.post_id).first()
    if not fetch_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {votepayload.post_id} is not found")

    vote_query = db.query(model.Vote).filter(model.Vote.post_id == votepayload.post_id,model.Vote.user_id==current_user.id)
    found_vote=vote_query.first()
    if votepayload.dir==1 :
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user-{current_user.id} has already voted for this post")
        new_vote=model.Vote(post_id=votepayload.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"vote added"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"vote deleted"}
    

