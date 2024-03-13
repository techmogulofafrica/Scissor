import hashing
import models, database
from models import User
from sqlalchemy.orm import Session
from database import engine, get_db
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, Request, Form


router = APIRouter()

session = Session(bind=engine)
models.Base.metadata.create_all(bind=database.engine)

templates=Jinja2Templates(directory="templates")


# ROUTE TO GET SIGNUP PAGE 
@router.get("/signup", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(request=request, name="signup.html")


# ROUTE TO CREATE SIGNUP
@router.post("/signup", response_class=HTMLResponse)
async def create_user(request:Request, db: Session =  Depends(get_db),
                      email: str = Form(...), username: str = Form(...),
                        first_name: str = Form(...), last_name: str = Form(...), password: str = Form(...), password2: str = Form(...)):
    

    validation1 = db.query(User).filter(User.username == username).first()
    
    validation2 = db.query(User).filter(User.email == email).first()


    if password != password2:
        msg = "Password does not match"
        return templates.TemplateResponse("signup.html", {"request": request, "msg": msg})
    
    elif validation1 is not None:
        msg = "User with username exist"
        return templates.TemplateResponse("signup.html", {"request": request, "msg": msg})
    
    elif validation2 is not None:
        msg = "User with email exist"
        return templates.TemplateResponse("signup.html", {"request": request, "msg": msg})
    
    user_model = models.User()
    user_model.email = email
    user_model.username = username
    user_model.first_name = first_name
    user_model.last_name = last_name
    user_model.hashed_password = hashing.Hash.bycrypt(password)

    db.add(user_model)
    db.commit()
    
    msg = "Register successfully"
    return templates.TemplateResponse("login.html", {"request": request, "msg": msg})