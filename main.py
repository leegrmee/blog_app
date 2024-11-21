from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from resources.exceptions import AppException
from resources.user.user_controller import router as user_router
from resources.article.article_controller import router as article_router
from resources.category.category_controller import router as category_router
from resources.comment.comment_controller import router as comment_router
from resources.like.like_controller import router as like_router
from resources.auth.auth_controller import router as auth_router
from resources.files.file_controller import router as file_router
from config.Connection import prisma_connection
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


app = FastAPI(lifespan=lifespan)

# 라우터 등록
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(article_router)
app.include_router(category_router)
app.include_router(comment_router)
app.include_router(like_router)
app.include_router(file_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


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


# 또한 FastAPI에서는 요청 데이터의 유효성 검사 실패 시 RequestValidationError 예외가 발생
# 이 예외에 대한 글로벌 핸들러를 정의하면, 클라이언트에게 일관된 형식으로 에러 메시지를 전달
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )
