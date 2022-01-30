
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from starlette.routing import Router
from sqlalchemy.orm import Session
from .. import models,schemas, oauth2
from ..database import get_db
from typing import List

router= APIRouter(
    prefix="/posts",
    tags=['posts']
)





    # db.query is the database object for querying 
    #the db While models.Post is refering to the table 
    # object define on models.py and .all() is to select All like *
  


#Reading as part of CRUD operation with SQL
@router.get("/", response_model=List[schemas.Post]) #Decorator
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return  posts

#Creating as part of CRUD operation  with SQL
@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post) #Decorator

# user_id: int=Depends(oauth2.get_current_user) forces  a user to login before they can create a post
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)): #post is just a variable that stores the class Post in this function
    print(current_user.email)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#Reading specific item as part of CRUD operation  with SQL
@router.get("/{id}", response_model=schemas.Post) #Decorator to get specific id from the user, the id means a path parameter
def get_post(id: int, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post


#Deleting specific item as part of CRUD operation  with SQL
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    
    post.delete(synchronize_session = False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)



#Updating specific item as part of CRUD operation with SQL
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post )
def  update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()
    if post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    post_query.update(updated_post.dict(), synchronize_session=False)
    
    db.commit()
    return  post_query.first()