import asyncio

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import get_settings

settings = get_settings()

SQLALCHEMY_DATABASE_URL = "mysql+mysqldb://" f"{settings.database_username}:{settings.database_password}" "@127.0.0.1/fastapi-ca"
ASYNC_SQLALCHEMY_DATABASE_URL = "mysql+asyncmy://" f"{settings.database_username}:{settings.database_password}" "@127.0.0.1/fastapi-ca"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async_engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL, echo=True, pool_size=10, max_overflow=20, pool_timeout=30)
session_factory = async_sessionmaker(bind=async_engine)
AsyncSessionLocal = async_scoped_session(session_factory, scopefunc=asyncio.current_task)

Base = declarative_base()
