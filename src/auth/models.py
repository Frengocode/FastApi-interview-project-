from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.database import Base
from datetime import datetime



class User(Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    books: Mapped['Book'] = relationship('Book')
    registared_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())
    