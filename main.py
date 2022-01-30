from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel

from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import now

from app.router.auth import login
from . import models,schemas, utils
from .database import engine, get_db
from sqlalchemy import delete

from .router import post, user,auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()




while True:

    try:
    # Connecting to an existing database
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
        password='Magfum12', cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("connection failed to Db")
        print("Error:",  error)
        #suspends execution for the given number of seconds-2sec if an error is encountered
        time.sleep(2)


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title":"favourate foods", "content": "I like Pizza", "id": 2}]

#looping through a list of python distionary to find specific items(id) so that it can be deleted
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

#looping through a list of python distionary to find specific dictionary (id) and return it index so that it can be updated
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

#Reading as part of CRUD operation            
@app.get("/") #Decorator
def root():
    return {"message": "Hello World"}