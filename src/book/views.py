from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.auth import get_current_user
from .models import Book
from fastapi import APIRouter, HTTPException, Depends
from src.auth.models import User
from .schemas import BookCreate, BookResponse, BookStatusUpdate
from sqlalchemy import select
from src.core.db_helper import db_helper
from typing import List

book_router = APIRouter(tags=["Book"])


@book_router.post("/create-book/")
async def create_book(
    request: BookCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
    current_user: User = Depends(get_current_user),
):

    new_book = Book(
        title=request.title,
        year=request.year,
        author=request.author,
        book_creator_id=current_user.id,
    )

    session.add(new_book)
    await session.commit()
    return new_book


@book_router.get("/get-book-with-id/{book_id}/", response_model=BookResponse)
async def get_book_with_id(
    book_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
    current_user: User = Depends(get_current_user),
):

    book = await session.execute(select(Book).filter(Book.id == book_id))

    book_result = book.scalars().first()
    if not book_result:
        raise HTTPException(detail="Not Found", status_code=404)

    return book_result


@book_router.delete("/delete-book/{book_id}/")
async def delete_book(
    book_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session),
    current_user: User = Depends(get_current_user),
):

    book = await session.execute(
        select(Book)
        .filter(Book.book_creator_id == current_user.id)
        .filter(Book.id == book)
    )

    book_result = book.scalars().first()
    if not book_result:
        raise HTTPException(detail="Not found", status_code=404)

    await session.delete()
    await session.commit()
    return "Book Deleted"


@book_router.get("/get-all-books/", response_model=List[BookResponse])
async def get_all_books(
    session: AsyncSession = Depends(db_helper.session_dependency),
    current_user: User = Depends(get_current_user),
) -> List[BookResponse] | None:

    books = await session.execute(select(Book).order_by(Book.year.desc()))
    result = books.scalars().all()

    return result


@book_router.put("/update-book/", response_model=BookStatusUpdate)
async def update_book_status(
    request: BookStatusUpdate,
    book_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
    current_user: User = Depends(get_current_user),
):

    book = await session.execute(
        select(Book)
        .filter(Book.id == book_id)
        .filter(Book.book_creator_id == current_user.id)
    )

    result = book.scalars().first()
    if not result:
        raise HTTPException(detail="Not Found", status_code=404)

    result.status = request.status

    await session.commit()
    return result


@book_router.get("/search-books/", response_model=List[BookResponse])
async def search_books(
    title: str = None,
    year: int = None,
    session: AsyncSession = Depends(db_helper.session_dependency),
    current_user: User = Depends(get_current_user),
) -> List[BookResponse]:
    query = select(Book)

    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))

    if year:
        query = query.filter(Book.year == year)

    query = query.order_by(Book.year.desc())

    books = await session.execute(query)
    result = books.scalars().all()

    return result
