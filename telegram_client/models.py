from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, declared_attr

from .constants import MAX_NAME_LENGTH, TOKEN_LENGTH


class Base(DeclarativeBase):

    @declared_attr
    def __tablename__(cls):  # pylint: disable=no-self-argument
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


class TelegramUser(Base):
    username = Column(String(MAX_NAME_LENGTH), nullable=True)
    tg_user_id = Column(Integer)
    token = Column(String(TOKEN_LENGTH), nullable=True)
