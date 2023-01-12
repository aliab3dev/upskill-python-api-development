from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("", response_model=List[schemas.Post])
def get_posts(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = None,
):
    # print(current_user.email)
    posts = (
        db.query(models.Post)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    return posts


@router.get("/{id}", response_model=schemas.Post)
def get_posts(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found!",
        )

    return post


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
    post: schemas.PostBase,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):

    new_post = models.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    updated_post: schemas.PostBase,
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found!",
        )
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"not authorized to perform the requested action!",
        )

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found!",
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"not authorized to perform the requested action!",
        )

    post_query.delete(synchronize_session=False)
    db.commit()
