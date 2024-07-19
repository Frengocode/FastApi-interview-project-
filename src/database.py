from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declared_attr


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return f'{cls.__name__.lower()}s'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)