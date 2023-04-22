import random
from time import sleep
from typing import Optional
from fastapi import Depends, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from app import model
from .database import SessionLocal, engine, get_db

model.Base.metadata.create_all(bind=engine)
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


# old code for db connection
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastApi',
#                                 user='postgres', password='1234', cursor_factory=RealDictCursor)
#         cur = conn.cursor()
#         print('database connected')
#         break
#     except Exception as error:
#         print("Connection to db was failed", error)
#         sleep(2)


# my_post = [{"title": "hello", "content": "hi", "id": 12}]


# def find_post(id):
#     for key in my_post:
#         if key["id"] == id:
#             return key


# def delet_post(id):
#     for i in range(len(my_post)):
#         if my_post[i]["id"] == id:
#             del my_post[i]
#             break


# def updated_post(payload):
#     for i in range(len(my_post)):
#         if my_post[i]["id"] == payload["id"]:
#             my_post[i] = payload
#             break


# @app.get("/")
# def root():
#     return {"message": "Hello world"}

@app.get("/sql")
def root(db: Session = Depends(get_db)):
    all_post=db.query(model.Post).all()
    return {"message": all_post}


# @app.get("/posts")
# def get_post():
#     cur.execute("""SELECT * FROM post """)
#     post = cur.fetchall()
#     return {"message": post}


# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_post(payload: Post):
#     # new_post = payload.dict()
#     # new_post["id"] = random.randrange(0, 100)
#     # my_post.append(new_post)
#     cur.execute("""INSERT INTO post(title,content,published) VALUES (%s,%s,%s) RETURNING * """,
#                 (payload.title, payload.content, payload.published))
#     new_post = cur.fetchone()
#     conn.commit()
#     return {"post created": new_post}


# @app.get("/posts/{id}")
# def get_specific_post(id: int, response: Response):
#     # if not find_post(id):
#     #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#     #                         detail=f"post with id: {id} is not found")
#     #     # response.status_code=status.HTTP_404_NOT_FOUND
#     #     # return {"messgae":f"post with id:{id} is not found"}
#     # return {"data": find_post(id)}
#     cur.execute("""Select * from post where id=%s""", (str(id),))
#     fetch_post = cur.fetchone()
#     if not fetch_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} is not found")
#     return {"data": fetch_post}


# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_specific_post(id: int):
#     cur.execute("""DELETE from post where id=%s RETURNING * """, (str(id),))
#     delete_post = cur.fetchone()
#     conn.commit()
#     if not delete_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} is not found")


# @app.put("/posts/{id}")
# def update_specific_post(id: int, payload: Post):
#     # if not find_post(id):
#     #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#     #                         detail=f"post with id: {id} is not found")
#     #     # response.status_code=status.HTTP_404_NOT_FOUND
#     #     # return {"messgae":f"post with id:{id} is not found"}
#     # new_post = payload.dict()
#     # new_post["id"] = id
#     # updated_post(new_post)
#     # return {"data": f"post {id} has been updated"}
#     cur.execute("""UPDATE post SET title=%s,content=%s,published=%s WHERE id=%s RETURNING * """,
#                 (payload.title, payload.content, payload.published, str(id)))
#     update_post = cur.fetchone()
#     conn.commit()
#     if not update_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} is not found")
#     return {"post created": update_post}

