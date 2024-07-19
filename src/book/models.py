from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, ForeignKey
from src.database import Base
from datetime import datetime
from sqlalchemy_utils import ChoiceType
from .schemas import EnumForBook

class Book(Base):
    __tablename__ = 'books'

    title: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    author: Mapped[str] = mapped_column(String, nullable=False)
    book_creator_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    status: Mapped[EnumForBook] = mapped_column(ChoiceType(EnumForBook), default=EnumForBook.Available)

    def __init__(self, title=None, year=None, status=EnumForBook.Available, author=None, book_creator_id=None):
        self.title = title
        self.year = year or datetime.utcnow()
        self.status = status
        self.author = author
        self.book_creator_id = book_creator_id

    def __repr__(self):
        return f'<Book(title={self.title}, author={self.author}, year={self.year}, status={self.status})>'
