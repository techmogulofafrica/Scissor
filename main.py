import models, database
from sqlalchemy.orm import Session
from database import engine
from routers.url_router import router as url_router
from routers.home_router import router as home_router
from routers.login_router import router as login_router
from routers.qr_codes import router as qr_codes_router
from routers.sign_up_router import router as sign_up_router
from routers.dashboard_router import router as dashboard_router
from routers.logout_router import router as logout_router
from routers.redirect_router import router as redirect_router
from starlette.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException as StarletteHTTPException
from fastapi import FastAPI, Request
from fastapi_simple_cache.backends.inmemory import InMemoryBackend
from fastapi_simple_cache import FastAPISimpleCache



app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

templates=Jinja2Templates(directory="templates")

session = Session(bind=engine)
models.Base.metadata.create_all(bind=database.engine)


app.include_router(router=home_router, prefix="", tags=["Home"])
app.include_router(router=url_router, prefix="/url", tags=["Url"])
app.include_router(router=login_router, prefix="/auth", tags=["Auth"])
app.include_router(router=qr_codes_router, prefix="/qrcode", tags=["Auth"])
app.include_router(router=sign_up_router, prefix="/auth", tags=["Auth"])
app.include_router(router=logout_router, prefix="/auth", tags=["Auth"])
app.include_router(router=dashboard_router, prefix="/dashboard", tags=["User"])
app.include_router(router=redirect_router, prefix="", tags=["Redirect"])



@app.on_event("startup")
async def startup():
    backend = InMemoryBackend()
    FastAPISimpleCache.init(backend=backend)



# GLOBAL ERROR HANDLING
@app.exception_handler(StarletteHTTPException)
async def my_custom_exception_handler(request: Request, exc: StarletteHTTPException):

    if exc.status_code == 404:
        return templates.TemplateResponse('404.html', {
            'request': request,
             'detail': exc.detail
             })
    
    
    elif exc.status_code == 401:
        msg = "Login to continue"
        return templates.TemplateResponse('login.html', {
            'request': request,
            "msg":msg,
            'detail': exc.detail
        })
    
    elif exc.status_code == 429:
        return templates.TemplateResponse('429.html', {
            'request': request,
            'detail': exc.detail
        })
    
    else:
        return templates.TemplateResponse('404.html', {
            'request': request,
            'detail': exc.detail
        })
    
