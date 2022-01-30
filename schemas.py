from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from sqlalchemy.sql.sqltypes import DateTime # for setting field validation
from typing import Optional
#All that is done here is to validate both request and response messages to ad from the API

#setting up schemas/pandentic to handle field validations for post request messages
class Post(BaseModel):
    
    title: str
    content: str
    Published: bool = True


class PostBase(BaseModel):
    title: str
    content: str
    Published: bool = True

class PostCreate(PostBase):
    pass




#setup schems/pandentic to handle field validation of response messages and inherite other fields in PostBase
class Post(PostBase):
    created_at: datetime

    #This subclass Config takes a SQLAlchemy model and converts it into a dictionary so that pandentic can work with it in the response message.
    class Config:
        orm_mode = True








#setting up schemas/pandentic to handle field validations for user creation request messages
class UserCreate(BaseModel):
    email: EmailStr
    password: str


#setup schems/pandentic to handle field validation of response messages for user creation and inherite other fields in u
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    #This subclass Config takes a SQLAlchemy model and converts it into a dictionary so that pandentic can work with it in the response message.
    class Config:
        orm_mode = True





#setting up schemas/pandentic to handle field validations for user login request messages
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
