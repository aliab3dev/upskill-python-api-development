from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(prefix="/votes", tags=["Votes"])


@router.get("", response_model=List[schemas.Vote])
def get_votes(db: Session = Depends(get_db)):

    votes = db.query(models.Vote).all()

    return votes


@router.post("", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.VoteBase,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post {vote.post_id} does not exist!",
        )

    # query vote
    vote_query = db.query(models.Vote).filter(
        models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id
    )

    existing_vote = vote_query.first()

    if vote.dir == 1:
        if existing_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already voted on post {vote.post_id}!",
            )
        # create vote
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote!"}

    elif vote.dir == 0:
        # check if vote exists
        if not existing_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist!"
            )
        # delete vote
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully removed vote!"}
