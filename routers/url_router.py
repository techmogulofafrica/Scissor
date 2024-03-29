import io
import random
import string
import qrcode
from base64 import b64encode
from fastapi import APIRouter, Depends, status, Request, Form
from typing import Optional
import models, database
from sqlalchemy.orm import Session
from database import engine, get_db
from models import URL
from starlette.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from token_file_Oauth2 import get_current_user
from fastapi_simple_rate_limiter import rate_limiter
from fastapi_simple_cache.decorator import cache



router = APIRouter()

session = Session(bind=engine)
models.Base.metadata.create_all(bind=database.engine)

templates=Jinja2Templates(directory="templates")



# FUNCTION TO GENERATE SHORT URL
def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url

# FUNCTION TO GENERATE QRCODE
def generateQR(full_shorten_url: str):
    img = qrcode.make(full_shorten_url)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    base64_img = "data:image/png;base64," +  b64encode(buf.getvalue()).decode('ascii')
    return base64_img



# ROUTE TO GET ALL URLS GENERATED BY A USER
@router.get("/my_urls", response_class=HTMLResponse)
@rate_limiter(limit=10, seconds=10)
@cache(expire=10) 
async def get_all_urls_by_user(request: Request, db: Session = Depends(get_db)):

    user = await get_current_user(request)
    if user is None:
        return RedirectResponse("/auth/login", status_code=status.HTTP_302_FOUND)

    urls = db.query(URL).filter(URL.owner_id == user.get("id")).all()
    return templates.TemplateResponse("links.html", {"request": request, "urls": urls, "user":user})





# ROUTE TO GET HTML PAGE TO EDIT URL
@router.get("/edit/{url_id}", response_class=HTMLResponse)
@rate_limiter(limit=10, seconds=10)
@cache(expire=60) 
async def edit_url_FE(request: Request, url_id= int, db: Session = Depends(get_db)):

    user = await get_current_user(request)
    if user is None:
        return RedirectResponse("/auth/login", status_code=status.HTTP_302_FOUND)

    url = db.query(URL).filter(URL.id == url_id).first()
    return templates.TemplateResponse("edit_url.html", {"request": request, "url" : url, "user": user})


# ROUTE TO EDIT URL
@router.post("/edit/{url_id}", response_class=RedirectResponse)
async def edit_url_BE(request: Request, url_id:int, db: Session = Depends(get_db),
                     title: str = Form(...), original_url: str = Form(...),
                            custom_alias: Optional[str] = Form(None)):
    

    user = await get_current_user(request)
    if user is None:
        return RedirectResponse("/auth/login", status_code=status.HTTP_302_FOUND)

    url = db.query(models.URL).filter(models.URL.id == url_id).first()
    
    
    url.short_url = url.short_url
    url.title = title
    url.custom_alias = url.custom_alias
    url.original_url = url.original_url
    url.qrcode = url.qrcode
    
    db.add(url)
    db.commit()

    return RedirectResponse("/url/my_urls", status_code=status.HTTP_302_FOUND)





# ROUTE TO GET HTML PAGE TO CREATE URL
@router.get("/create", response_class=HTMLResponse)
@rate_limiter(limit=10, seconds=10)
@cache(expire=60) 
async def create_url_FE(request: Request):

    user = await get_current_user(request)
    if user is None:
        return RedirectResponse("/auth/login", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse("create.html", {"request": request})


# ROUTE TO CREATE URL
@router.post("/create", response_class=HTMLResponse)
async def create_url_BE(request:Request, db: Session = Depends(get_db),
                 title: Optional[str] = Form(None), original_url: str = Form(...),
                            custom_alias: Optional[str] = Form(None)):

    user = await get_current_user(request)
    if user is None:
        return RedirectResponse("/auth/login", status_code=status.HTTP_302_FOUND)


    validation = db.query(URL).filter(URL.custom_alias == custom_alias).first()
   

    if custom_alias:
        url_model = models.URL()
        url_model.original_url = original_url
        url_model.title = title

        if validation is not None:
            msg = "Custom alias exist"
            return templates.TemplateResponse("create.html", {"request": request, "msg": msg})
        
        url_model.custom_alias = custom_alias
        url_model.owner_id = user.get("id")
        url_model.qrcode = generateQR("https://scissor-y0gc.onrender.com" + "/" + custom_alias)

    else: 
        short_url = generate_short_url()
        db_short_url = session.query(URL).filter(URL.short_url==short_url).first()
    
        if db_short_url is None:
            short_url == short_url
        else:
            while short_url in db_short_url:
                short_url = generate_short_url()
            
        url_model = models.URL()
        url_model.original_url = original_url
        url_model.title = title
        url_model.short_url = short_url
        url_model.owner_id = user.get("id")
        url_model.qrcode = generateQR("https://scissor-y0gc.onrender.com" + "/" + short_url)

    db.add(url_model)
    db.commit()
    
    return RedirectResponse("/url/my_urls", status_code=status.HTTP_302_FOUND)



# ROUTE TO DELETE URL
@router.get("/delete/{url_id}", response_class=HTMLResponse)
@rate_limiter(limit=10, seconds=10)
async def delete_url(request:Request, url_id: int, db: Session = Depends(get_db)):
    
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse("/auth/login", status_code=status.HTTP_302_FOUND)
    
    url_model = db.query(URL).filter(URL.id == url_id).filter(URL.owner_id == user.get("id")).first()
    
    if url_model is None:
        return RedirectResponse("/url/my_urls", status_code=status.HTTP_302_FOUND)
    
    db.delete(url_model)
    db.commit()
    
    return RedirectResponse("/url/my_urls", status_code=status.HTTP_302_FOUND)
