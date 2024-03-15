import models, database
from database import engine
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from token_file_Oauth2 import get_current_user
from starlette.responses import RedirectResponse
from fastapi import APIRouter, Request, status
from fastapi_simple_rate_limiter import rate_limiter
from fastapi_simple_cache.decorator import cache


router = APIRouter()

session = Session(bind=engine)
models.Base.metadata.create_all(bind=database.engine)

templates=Jinja2Templates(directory="templates")



# ROUTE TO GET HTML FOR  USER DASHBOARD
@router.get("/user", response_class=HTMLResponse)
@rate_limiter(limit=5, seconds=10)
@cache(expire=3600) 
async def user_dashboard_FE(request: Request):

    user = await get_current_user(request)
    if user is None:
        return RedirectResponse("/auth/login", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse(request=request, name="dashboard.html")
