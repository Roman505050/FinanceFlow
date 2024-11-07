from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)
from sqlalchemy.pool import NullPool


from config import POSTGRES_URI


async_engine = create_async_engine(POSTGRES_URI, poolclass=NullPool)
async_session_maker = async_sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)


class SessionContextManager:
    def __init__(self):
        self.session: AsyncSession

    async def __aenter__(self) -> AsyncSession:
        self.session = async_session_maker()
        return self.session

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.session.close()
