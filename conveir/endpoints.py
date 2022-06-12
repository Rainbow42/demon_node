from fastapi import APIRouter, Body, Depends, Path, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from conveir import schemas
from conveir.models import Transporter
from utils import get_session

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
    instance = Transporter(**data)
    await db_session.execute(instance)
    return data


# @router.post(path='/pipeline/',
#              name='Создания сценариев конвейера',
#              description='создания сценариев конвейера',
#              operation_id='api_save_pipeline',
#              tags=['Pipeline'],
#              response_model=schemas.Pipeline,
#              status_code=200)
# async def save_pipeline(
#         data: schemas.Pipeline = Body(..., title='Данные о сценарии'),
#         db_session: AsyncSession = Depends(get_session),
#         request: Request = None
# ):
#     instance = Transporter(**data)
#     await db_session.execute(instance)
#     return data


