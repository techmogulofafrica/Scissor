from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:QWe45YU.@localhost:5432/ScissorApplicationDatabase"
# SQLALCHEMY_DATABASE_URL = "postgresql://gvpzdzwi:4Kh0inaihxsQMl-UgQKW2xQztDNtilSj@ziggy.db.elephantsql.com/gvpzdzwi"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()