from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from .celery_app import celery_app
from src.core.db_helper import db_helper
from src.book.models import Book

@celery_app.task
async def delete_old_books():
    async with db_helper.session_dependency() as session:
        async with session.begin():
            one_day_ago = datetime.utcnow() - timedelta(days=1)
            stmt = delete(Book).where(Book.year < one_day_ago)
            await session.execute(stmt)
            await session.commit()
