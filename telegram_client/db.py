import asyncio
from os import getenv

from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

load_dotenv()

ENGINE = create_async_engine(getenv('ENGINE'))
Base = declarative_base()


class TgUser(Base):
    __tablename__ = __name__.lower()
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(256))
    token = Column(String(256), nullable=True)
    tg_user_id = Column(Integer)


async def init_models():
    async with ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_models())
