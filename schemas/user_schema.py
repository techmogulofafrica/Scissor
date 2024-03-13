from pydantic import BaseModel, EmailStr, Field
from typing import List
from schemas.url_schema import DisplayURL

class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str 
    email: EmailStr
    password: str
    urls : List[DisplayURL] = []
    is_active:bool

class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str 
    email: EmailStr
    
class User(UserBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True



class Login(BaseModel):
    username: str
    password: str  


class Signup(BaseModel):
    first_name: str
    last_name: str
    email : EmailStr
    username: str
    password: str 
    password2: str
    
    class config:
        from_attributes = True