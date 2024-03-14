from fastapi import APIRouter, Request
import models, database
from sqlalchemy.orm import Session
from database import engine
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_simple_rate_limiter import  rate_limiter


router = APIRouter()

session = Session(bind=engine)
models.Base.metadata.create_all(bind=database.engine)

templates=Jinja2Templates(directory="templates")

# ROUTE TO LOGOUT A USER
@router.get("/logout", response_class=HTMLResponse)
@rate_limiter(limit=5, seconds=30)
async def logout(request: Request):

    msg = "Logout successfully"
    response = templates.TemplateResponse("login.html", {"request": request, "msg": msg})
    response.delete_cookie(key="access_token")

    return response
