from models import URL
import models, database
from sqlalchemy.orm import Session
from database import engine, get_db
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from token_file_Oauth2 import get_current_user
from fastapi import APIRouter, Request, Depends, status


router = APIRouter()

session = Session(bind=engine)
models.Base.metadata.create_all(bind=database.engine)

templates=Jinja2Templates(directory="templates")


# ROUTE USED TO LIST  ALL QRCODE BY USER
@router.get("/qr", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):

    user = await get_current_user(request)
    if user is None:
        return RedirectResponse("/auth/login", status_code=status.HTTP_302_FOUND)
    
    urls = db.query(URL).filter(URL.owner_id == user.get("id")).all()

    return templates.TemplateResponse("qrcode.html", {"request": request , "urls": urls, "user":user})

