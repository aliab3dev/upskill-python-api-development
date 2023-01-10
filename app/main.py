from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return posts


@app.get("/posts/{id}", response_model=schemas.Post)
def get_posts(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found!",
        )

    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostBase, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(post: schemas.PostBase, id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found!",
        )
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found!",
        )

    post_query.delete(synchronize_session=False)
    db.commit()


@app.get("/users", response_model=List[schemas.User])
def get_posts(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    return users


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
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


