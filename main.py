from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.core.exceptions.base import AppException
from src.api.v1.auth.auth_controller import router as auth_router
from src.api.v1.users.user_controller import router as user_router
from src.api.v1.articles.article_controller import router as article_router
from src.api.v1.categories.category_controller import router as category_router
from src.api.v1.comments.comment_controller import router as comment_router
from src.api.v1.likes.like_controller import router as like_router
from src.api.v1.files.file_controller import router as file_router
from src.core.database.connection import prisma_connection
import logging


logging.basicConfig(level=logging.ERROR)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Startup
    print("Start Server")
    await prisma_connection.connect()
    yield
    # Shutdown
    print("Shutdown Server")
    await prisma_connection.disconnect()


app = FastAPI(
    title="Blog API",
    description="A modern blog API built with FastAPI and Prisma",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API v1 prefix
API_V1_PREFIX = "/api/v1"

# API 라우터 등록
app.include_router(auth_router, prefix=API_V1_PREFIX)
app.include_router(user_router, prefix=API_V1_PREFIX)
app.include_router(article_router, prefix=API_V1_PREFIX)
app.include_router(category_router, prefix=API_V1_PREFIX)
app.include_router(comment_router, prefix=API_V1_PREFIX)
app.include_router(like_router, prefix=API_V1_PREFIX)
app.include_router(file_router, prefix=API_V1_PREFIX)


@app.get("/")
async def root():
    return {"message": "Welcome to Blog API", "version": "1.0.0", "docs": "/docs"}


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    logging.error(f"AppException occurred: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        # HTTPException은 FastAPI의 기본 핸들러로 넘김
        raise exc
    logging.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )
