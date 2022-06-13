from typing import Type, TypeVar, Any

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.db.base_class import Base
from application.db.session import SessionLocal

ModelType = TypeVar('ModelType', bound=Base)


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


async def get_by_id_or_exception(db_session: AsyncSession,
                                 model: Type[ModelType],
                                 instance_id: Any):
    cursor = await db_session.execute(select(model).
                                      where(model.id == instance_id))
    instance = cursor.scalars().first()
    if not instance:
        raise HTTPException(status_code=404,
                            detail=f'{model.id} = {instance_id} не существует!')

    return instance


async def exists_model(db_session: AsyncSession,
                       model: Type[ModelType],
                       instance_id: Any):
    cursor = await db_session.execute(select(model).
                                      where(model.id_repositories == instance_id))

    instance = cursor.scalars().first()
    if instance:
        raise HTTPException(status_code=404,
                            detail=f'{model.__name__} = {instance_id} уже существует!')
