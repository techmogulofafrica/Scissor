import models, database
from hashing import Hash
from typing import Optional
from sqlalchemy.orm import Session
from datetime import timedelta
from database import engine, get_db
from sqlalchemy.orm import Session
from schemas.token_schema import Token
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from token_file_Oauth2 import create_access_token
from starlette.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Request,  Depends, HTTPException, status, Response
from fastapi_simple_rate_limiter import rate_limiter
from fastapi_simple_cache.decorator import cache


router = APIRouter()


session = Session(bind=engine)
models.Base.metadata.create_all(bind=database.engine)

templates=Jinja2Templates(directory="templates")


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None
        
    async def create_outh_form(self):
        form =  await self.request.form()
        self.username = form.get("username")
        self.password = form.get("password")
        



@router.post("/token", response_model=Token)
async def login_for_access_token(response: Response, 
                                 request: OAuth2PasswordRequestForm = Depends(), 
                                 db: Session = Depends(get_db)):
    user =  db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        return False
    if not Hash.verify(request.password, user.hashed_password):
        return False
    
    access_token = create_access_token(user.username, user.id, timedelta(minutes=30))
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return True


# ROUTE TO GET HTML PAGE FOR LOGIN
@router.get("/login", response_class=HTMLResponse)
@rate_limiter(limit=10, seconds=10)
@cache(expire=3600) 
async def login_FE(request: Request):

    return templates.TemplateResponse(request=request, name="login.html")


# ROUTE TO LOGIN USER
@router.post("/login", response_class=HTMLResponse)
async def login_BE(request:Request, db: Session = Depends(get_db)):
    
    try:
        form = LoginForm(request)
        await form.create_outh_form()
        response = RedirectResponse(url="/dashboard/user", status_code=status.HTTP_302_FOUND)
        
        validate_user_cookie = await login_for_access_token(response = response, request = form, db = db)
        if not validate_user_cookie:
            msg = "Invalid username or password"
            return templates.TemplateResponse("login.html", {"request": request, "msg":msg})
        else:
            return response
        
    except HTTPException:
        msg = "unknown error"
        return templates.TemplateResponse("login.html", {"request": request, "msg":msg})
