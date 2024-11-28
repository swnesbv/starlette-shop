
from __future__ import annotations

from datetime import datetime

from typing_extensions import Annotated

from sqlalchemy import String, DateTime, ForeignKey, Text, JSON

from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableList

from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column

from db_config.settings import settings


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL
)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


intpk = Annotated[int, mapped_column(primary_key=True, index=True)]
chapter = Annotated[str, mapped_column(String(30), unique=True, index=True)]
affair = Annotated[str, mapped_column(Text, nullable=True)]
pictures = Annotated[str, mapped_column(String, nullable=True)]
allcts = Annotated[dict | list, mapped_column(
    MutableList.as_mutable(ARRAY(String(30))), nullable=True
)]
alljson = Annotated[dict | list, mapped_column(JSON, nullable=True)]
# ..
points = Annotated[datetime, mapped_column(DateTime, nullable=True)]
# ..
user_fk = Annotated[
    int, mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
]
tm_fk = Annotated[
    int, mapped_column(ForeignKey("item_tm.id", ondelete="CASCADE"), nullable=False)
]
