from functools import wraps
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (create_async_engine,
                                    AsyncEngine,
                                    async_sessionmaker,
                                    AsyncSession)

from src.config import settings

class Singleton(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

class Database(Singleton):
    def __init__(self,
                 url: str,
                 echo: bool = False,
                 pool_size: int = 5,
                 max_overflow: int = 10):
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            pool_size=pool_size,
            max_overflow=max_overflow
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


database = Database(url=str(settings.db.url),
                    echo=settings.db.echo)

async def connection(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with database.session_factory() as session:
            try:
                result = await func(*args, session=session, **kwargs)
                await session.flush()
                await session.commit()
                return result
            except Exception as e:
                print("Error accessing the database. @connection")
                raise e
            finally:
                await session.close()
    return wrapper


