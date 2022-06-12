from sqlalchemy.ext.asyncio import AsyncSession

from application.db.session import SessionLocal


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
