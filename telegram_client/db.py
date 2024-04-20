from sqlalchemy import BigInteger, Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr

from .constants import DATABASE_URL, MAX_NAME_LENGTH, TOKEN_LENGTH

ENGINE = create_async_engine(DATABASE_URL)


class Base(DeclarativeBase):

    @declared_attr
    def __tablename__(cls):  # pylint: disable=no-self-argument
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


class TelegramUser(Base):
    username = Column(String(MAX_NAME_LENGTH), nullable=False)
    password = Column(String(TOKEN_LENGTH), nullable=False)
    tg_user_id = Column(BigInteger, nullable=False)
    token = Column(String(TOKEN_LENGTH), nullable=False)
