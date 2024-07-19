from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from .config import settings
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.asyncio import async_sessionmaker
from asyncio import current_task
from contextlib import asynccontextmanager

class DatabaseHelper:

    def __init__(self, url: str, echo: bool = True):
        self.engine = create_async_engine(url=url, echo=echo)
        
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )
        
        self.scoped_session = scoped_session(
            sessionmaker(bind=self.engine, class_=AsyncSession)
        )
    
    def get_scope_session(self):
        return self.scoped_session
    
    async def session_dependency(self):
        async with self.session_factory() as session:
            yield session

db_helper = DatabaseHelper(url=settings.db_url, echo=settings.db_echo)
