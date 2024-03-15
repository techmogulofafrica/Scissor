import models, database
from sqlalchemy.orm import Session
from database import engine, get_db
from schemas.url_schema import URLAnalytics
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, status, Request, status
from fastapi_simple_rate_limiter import rate_limiter
from fastapi_simple_cache.decorator import cache



router = APIRouter()

session = Session(bind=engine)
models.Base.metadata.create_all(bind=database.engine)

templates=Jinja2Templates(directory="templates")
    


# ROUTE TO REDIRECT SHORTENED URL TO ORIGINNAL URL
@router.get("/{url}")
@rate_limiter(limit=10, seconds=10)
@cache(expire=3600) 
async def redirect_url(request:Request, url = str,  db: Session = Depends(get_db)):
        
        url1 = db.query(models.URL).filter(models.URL.custom_alias == url).first()
        url2 = db.query(models.URL).filter(models.URL.short_url == url).first()


        if url1:
              original_url = url1.original_url

              def update_url_clicks( url : URLAnalytics, db: Session = Depends(get_db)):
                  url1.clicks +=  1
                  db.commit()
                  db.refresh(url1) 

              update_url_clicks(url, db)

              response = RedirectResponse(url = original_url, status_code=status.HTTP_302_FOUND)
              return response

        elif url2:
              original_url = url2.original_url
              
              def update_url_clicks( url : URLAnalytics, db: Session = Depends(get_db)):
                  url2.clicks +=  1
                  db.commit()
                  db.refresh(url2) 

              update_url_clicks(url, db)
              response =RedirectResponse(url = original_url, status_code=status.HTTP_302_FOUND)
              return response

        else:
           return templates.TemplateResponse("404.html", {"request": request})
        