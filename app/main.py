from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
import random
import time
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    # title: str, content: str
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="aliab3d",
            password="",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("db connection successful!")
        break

    except Exception as error:
        print("db connection failed!")
        print(f"error: {error}")
        time.sleep(2)


@app.get("/")
def root():
    return {"message": "hello world!"}


@app.get("/posts")
def get_posts():
    query = """SELECT * FROM posts"""
    cursor.execute(query)
    posts = cursor.fetchall()

    return {"data": posts}


@app.get("/posts/{id}")
def get_posts(id: int):
    query = """SELECT * FROM posts WHERE id = %s"""
    vars = (str(id))
    cursor.execute(query, vars)
    post = cursor.fetchone()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found!",
        )

    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    query = """INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *"""
    vars = (post.title, post.content, post.published)
    cursor.execute(query, vars)
    post = cursor.fetchone()
    conn.commit()
    # posts_table.append(item)
    return {"data": post}


@app.put("/posts/{id}")
def update_post(post: Post, id: int):

    statement = """UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *"""
    query = (post.title, post.content, post.published, str(id))
    cursor.execute(statement, query)
    post = cursor.fetchone()
    conn.commit()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found!",
        )

    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    statement = """DELETE FROM posts WHERE id = %s RETURNING *"""
    query = (str(id), )
    cursor.execute(statement, query)
    post = cursor.fetchone()
    conn.commit()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found!",
        )
    return {"data": post}

