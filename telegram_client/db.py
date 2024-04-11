from sqlalchemy.ext.asyncio import create_async_engine

from .constants import DATABASE_URL


async_engine = create_async_engine(DATABASE_URL)
