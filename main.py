import uvicorn
import models, database
import redis.asyncio as redis
from sqlalchemy.orm import Session
from fastapi_limiter import FastAPILimiter
from database import engine
from fastapi_limiter.depends import RateLimiter
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
from fastapi import FastAPI, Request, HTTPException, Depends, status



app = FastAPI()


# app = FastAPI(dependencies=[Depends(RateLimiter(times=5, seconds=10))])



app.mount("/static", StaticFiles(directory="static"), name="static")

templates=Jinja2Templates(directory="templates")

session = Session(bind=engine)
models.Base.metadata.create_all(bind=database.engine)


app.include_router(router=home_router, prefix="", tags=["home"])
app.include_router(router=url_router, prefix="/url", tags=["url"])
app.include_router(router=login_router, prefix="/auth", tags=["auth"])
app.include_router(router=qr_codes_router, prefix="/qrcode", tags=["auth"])
app.include_router(router=sign_up_router, prefix="/auth", tags=["auth"])
app.include_router(router=logout_router, prefix="/auth", tags=["auth"])
app.include_router(router=dashboard_router, prefix="/dashboard", tags=["user"])
app.include_router(router=redirect_router, prefix="", tags=["redirect"])





# GLOBAL RATE LIMITING
# if RateLimiter(times=3, seconds=10) is True :
#         raise HTTPException(status_code = status.HTTP_429_TOO_MANY_REQUESTS)

# @app.on_event("startup")
# async def startup():
#     redis_connection = redis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
#     await FastAPILimiter.init(redis_connection)

# if __name__ == "__main__":
#     uvicorn.run("main:app", debug=True, reload=True)



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
    
