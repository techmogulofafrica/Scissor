from pydantic import BaseModel, EmailStr, HttpUrl, PastDatetime
from typing import Optional

class URLBase(BaseModel):
    id: int
    short_url: str
    custom_alias: Optional[str] = None

class URL(BaseModel):
    id: int
    short_url: str
    custom_alias: Optional[str] = None
    clicks: int
    title: Optional[str] = None
    original_url: str
    date_time_created: PastDatetime
    click_location: str 


class CreateURL(BaseModel):
    title: Optional[str] = None
    original_url: str
    custom_alias: Optional[str] = None

class EditURL(BaseModel):
    id: int
    title: Optional[str] = None
    custom_alias: Optional[str] = None


class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str 
    email: EmailStr

class DisplayURL(BaseModel):
    id: int
    title: Optional[str] = None
    short_url: str
    original_url: str
    date_time_created: PastDatetime
    owner: UserBase
    
    class config():
        from_attributes = True


class URLAnalytics(BaseModel):
    clicks: int
    click_location: str