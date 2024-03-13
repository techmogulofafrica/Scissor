import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    username = Column(String, unique=True, index = True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    urls = relationship("URL", back_populates= "owner")


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key= True)
    qrcode = Column(String, nullable=True )
    short_url = Column(String, index=True, unique=True)
    custom_alias = Column(String, index=True, nullable=True, unique=True)
    original_url = Column(String, index=True)
    title = Column(String, index=True)
    clicks = Column(Integer, default=0)
    click_location = Column(String)
    date_time_created = Column(DateTime, default=datetime.datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates= "urls")
