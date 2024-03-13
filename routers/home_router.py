import models, database
from database import engine
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request



router = APIRouter()


session = Session(bind=engine)
models.Base.metadata.create_all(bind=database.engine)

templates=Jinja2Templates(directory="templates")


# ROUTE TO GET HTML HOME PAGE
@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    
    return templates.TemplateResponse("home.html", {"request": request})
