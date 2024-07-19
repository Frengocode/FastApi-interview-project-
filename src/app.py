from fastapi import FastAPI
from src.auth.views import user_router
from src.book.views import book_router
from .database import Base
from contextlib import asynccontextmanager
from src.core.db_helper import db_helper

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(book_router)
app.include_router(user_router)
