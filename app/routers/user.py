from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[schemas.User])
def get_posts(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    return users


@router.get("/{id}", response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id: {id} not found!",
        )
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):

    # store password hash
    print(user.password)
    hashed_password = utils.pwd_context.hash(user.password)
    print(type(hashed_password), hashed_password)
    user.password = hashed_password

    existing_user = (
        db.query(models.User).filter(models.User.email == user.email).first()
    )
    if existing_user is None:
        new_user = models.User(**user.dict())
        print(type(new_user))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"User: {new_user} created!")
        return new_user
    else:
        print(f"User: {existing_user} already exists!")
        return existing_user
