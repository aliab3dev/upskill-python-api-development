from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
import random

app = FastAPI()

posts_table = [{"id": 1, "title": "title 1", "content": "content 1"}]


class Post(BaseModel):
    # title: str, content: str
    title: str
    content: str
    published: bool = True


def find_post(id: int):
    for item in posts_table:
        if item["id"] == id:
            return item


def find_post_idx(id: int):
    for idx, item in enumerate(posts_table):
        if id == item["id"]:
            return idx


@app.get("/")
def root():
    return {"message": "hello world!"}


@app.get("/posts")
def get_posts():
    # select * from posts
    return {"data": posts_table}


@app.get("/posts/{id}")
def get_posts(id: int):
    # select * from posts
    item = find_post(id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found!",
        )

    return {"data": item}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    # post is a pydantic model
    # equivalent dictionary: post.dict()
    item = {
        "id": random.randint(0, 100000),
        "title": post.title,
        "content": post.content,
    }
    posts_table.append(item)
    return {"data": item}


@app.put("/posts/{id}")
def update_post(post: Post, id: int):
    idx = find_post_idx(id)

    if idx is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found!",
        )

    posts_table[idx] = {"id": id, **post.dict()}
    return {"data": f"post with id: {id} updated!"}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    idx = find_post_idx(id)

    if idx is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found!",
        )

    posts_table.pop(idx)
