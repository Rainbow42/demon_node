from fastapi import APIRouter, Body, Depends, Path, Request, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from conveir import schemas
from conveir.models import Transporter, TransporterRepositories
from repositories.models import Repositories
from utils.db import get_session

router = APIRouter()


@router.get(path='/test/',
            name='Test',
            description='Test',
            operation_id='api_Test',
            tags=['Test'],
            status_code=200)
async def tests():
    return "test"


@router.post(path='/pipeline/',
             name='Создания сценариев конвейера',
             description='создания сценариев конвейера',
             operation_id='api_save_pipeline',
             tags=['Pipeline'],
             response_model=schemas.Pipeline,
             status_code=200)
async def save_pipeline(
        data: schemas.Pipeline = Body(..., title='Данные о сценарии'),
        db_session: AsyncSession = Depends(get_session),
):
    transporter = Transporter(
        name=data.name,
        version=data.version,
        extended_pipline=data.extended_pipline
    )
    db_session.add(transporter)
    await db_session.flush()

    query = select(Repositories).where(Repositories.id_repositories == data.repositories_id)
    cur_repositories = await db_session.execute(query)
    repositories = cur_repositories.scalars().first()
    trans_repositories = TransporterRepositories(
        repositories_id=repositories.id,
        transporter_id=transporter.id
    )
    db_session.add(trans_repositories)
    await db_session.commit()
    return data

