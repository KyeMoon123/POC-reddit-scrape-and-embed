from utils.app_exceptions import AppExceptionCase
from fastapi import FastAPI
from routers import foo, redditRouter,TopicQueryRouter
from config.database import create_tables
from logger import init_logging

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from utils.request_exceptions import (
    http_exception_handler,
    request_validation_exception_handler,
)
from utils.app_exceptions import app_exception_handler

create_tables()
# setup loggers
init_logging()

app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, e):
    return await http_exception_handler(request, e)


@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request, e):
    return await request_validation_exception_handler(request, e)


@app.exception_handler(AppExceptionCase)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)


app.include_router(foo.router)
app.include_router(redditRouter.router)
app.include_router(TopicQueryRouter.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
