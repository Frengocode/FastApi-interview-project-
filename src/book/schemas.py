from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class EnumForBook(Enum):
    Issued = 'Выдано'
    Available = 'В наличии'
    


class BookCreate(BaseModel):
    title: str
    author: str
    year: datetime


class BookStatusUpdate(BaseModel):
    status: EnumForBook
    

    


class BookResponse(BaseModel):
    id: int
    book_creator_id: Optional[int] = None
    title: str
    author: str
    year: datetime
    status: EnumForBook
    