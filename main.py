from contextlib import asynccontextmanager
from fastapi import FastAPI
from resources.user.user_controller import router as user_router
from resources.article.article_controller import router as article_router
from resources.category.category_controller import router as category_router
from resources.comment.comment_controller import router as comment_router
from resources.like.like_controller import router as like_router
from resources.auth.auth_controller import router as auth_router
from config.Connection import prisma_connection
import logging

logging.basicConfig(level=logging.INFO)


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

app.include_router(user_router)
app.include_router(article_router)
app.include_router(category_router)
app.include_router(comment_router)
app.include_router(like_router)
app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
