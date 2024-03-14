import models, database
from database import engine
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request
from fastapi_simple_rate_limiter import rate_limiter
from fastapi_simple_cache import FastAPISimpleCache
from fastapi_simple_cache.decorator import cache




router = APIRouter()


session = Session(bind=engine)
models.Base.metadata.create_all(bind=database.engine)

templates=Jinja2Templates(directory="templates")


# ROUTE TO GET HTML HOME PAGE
@router.get("/", response_class=HTMLResponse)
@rate_limiter(limit=5, seconds=30)
@cache(expire=86400) 
async def home(request: Request):
    
    return templates.TemplateResponse("home.html", {"request": request})
