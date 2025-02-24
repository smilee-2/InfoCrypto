from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class UserSchemas(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=True)
    username: Mapped[int] = mapped_column(unique=True, nullable=True)
    password: Mapped[str] = mapped_column(unique=True, nullable=True)
    disabled: Mapped[bool] = mapped_column(unique=True, nullable=True)
    root: Mapped[str] = mapped_column(unique=True, nullable=True)

    coins: Mapped[list['CoinsFavoritesSchemas']] = relationship(back_populates='user')


class CoinsFavoritesSchemas(Base):
    __tablename__ = 'favorites'

    id: Mapped[int] = mapped_column(primary_key=True)
    coin_name: Mapped[str] = mapped_column(unique=True, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))

    user: Mapped['UserSchemas'] = relationship(back_populates='coins')
