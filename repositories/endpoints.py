import asyncio
from sqlalchemy.dialects.postgresql import insert

from fastapi import APIRouter, Body, Depends, Path, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from helpers.gitlab import GitLabHelpers
from repositories import schemas
from repositories.models import RepositoriesUsers, Repositories, \
    RepositoriesToken
from utils import get_session

router = APIRouter()


@router.post(path='/repositories/',
             name='Добавить новый репозиторий',
             description='Добавить новый репозиторий',
             operation_id='api_save_repositories',
             tags=['Repositories'],
             # response_model=schemas.Repositories,
             status_code=200)
async def save_repositories(
        data: schemas.Repositories = Body(..., title='Данные о сценарии'),
        request: Request = None,
        db_session: AsyncSession = Depends(get_session),
):
    gitlab_helpers = GitLabHelpers(request, data.reposition_token, data.id_repositories)
    tasks = [
        gitlab_helpers.get_users(to_dict=True),
        gitlab_helpers.get_detail_repositories()
    ]
    users, project = await asyncio.gather(*tasks)

    project = project.dict()
    user = users.get(data.user_id)
    insert_users = insert(RepositoriesUsers).values(**user.dict())
    do_update_users = insert_users.on_conflict_do_update(
        index_elements=[RepositoriesUsers.id],
        set_=user.dict()
    )
    await db_session.execute(do_update_users)
    await db_session.flush()

    instance_rep = Repositories(
        id_repositories=project.get("id"),
        name=project.get("name"),
        description=project.get("description"),
        created_at=project.get("created_at").replace(tzinfo=None)
    )

    instance_token = RepositoriesToken(
        user_id=data.user_id,
        repositories_id=data.id_repositories,
        private_token=data.reposition_token
    )
    db_session.add_all([instance_rep, instance_token])

    await db_session.commit()
    return project


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


