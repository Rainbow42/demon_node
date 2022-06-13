import asyncio
from collections import defaultdict

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from application.celery import app
from application.db.session import SessionLocal
from helpers.gitlab import GitlabHelpersNoRequest
from repositories.models import Repositories, MergeRequest, RepositoriesToken, \
    RepositoriesUsers


def get_mrs(repositories, repositories_tokens) -> dict:
    loop = asyncio.get_event_loop()

    news_mrs_rep = dict()
    for rep_id, id_repositories in repositories.items():
        token = repositories_tokens.get(rep_id)
        gitlab_helpers = GitlabHelpersNoRequest(token, id_repositories)
        tasks = [
            gitlab_helpers.get_merge_requests()
        ]

        mrs = loop.run_until_complete(asyncio.gather(*tasks))
        news_mrs_rep[id_repositories] = mrs[0]
    return news_mrs_rep


def add_mr_or_start_pipline(session: SessionLocal,
                            news_mrs_rep: dict,
                            mrs_ids: dict,
                            sync):
    for rep_id, new_mrs in news_mrs_rep.items():
        for new_mr in new_mrs:
            old_mr = mrs_ids.get(new_mr.id)
            if old_mr and new_mr.updated_at > old_mr.updated_at \
                    and new_mr.state == 'opened':
                pass  # отправить в конвейер
            elif not old_mr:
                pass  # отправить в конвейер

            author = new_mr.author.dict()
            insert_user = insert(RepositoriesUsers).values(**author)
            do_update_user = insert_user.on_conflict_do_update(
                index_elements=[RepositoriesUsers.id],
                set_=author
            )
            sync(session.execute(do_update_user))
            sync(session.flush())

            new_mr = new_mr.dict(exclude_unset=True, exclude={"author"})
            new_mr["author_id"] = author.get("id")

            query = select(Repositories.id).where( Repositories.id_repositories==rep_id)
            repositories = sync(session.execute(query)).scalars().first()

            new_mr["repositories_id"] = repositories
            insert_user = insert(MergeRequest).values(**new_mr)
            do_update_user = insert_user.on_conflict_do_update(
                index_elements=[MergeRequest.id],
                set_=new_mr
            )
            sync(session.execute(do_update_user))
            sync(session.commit())


@app.task(shared=True)
def check_update_merge_request():
    """
    Обновляем данные о MР-по проектам
    1) Если мр со статусом открыт, и уже существует запись о нем,
    то проверяем дату обновления, если она позже чем текущая,
    то мр с его ветки нужно отдать конвейеру
    2) Если мр нет в системе, то они новые, добавляем запись в бд,
    если они открытые, то отдаем конвейеру
    """
    session = SessionLocal()
    loop = asyncio.get_event_loop()
    sync = loop.run_until_complete

    query = select(Repositories.id, Repositories.id_repositories)
    repositories = sync(session.execute(query)).fetchall()

    repositories_ids = {rep.id: rep.id_repositories for rep in repositories}

    rep_ids = list(repositories_ids.keys())

    mrs_query = select(MergeRequest).where(
        MergeRequest.repositories_id.in_(rep_ids)
    )
    mrs = sync(session.execute(mrs_query)).scalars().all()

    tokens_query = select(RepositoriesToken).where(
        RepositoriesToken.repositories_id.in_(rep_ids)
    )
    tokens = sync(session.execute(tokens_query)).scalars().all()

    mrs_ids = {mr.id: mr for mr in mrs}
    repositories_tokens = {token.repositories_id: token.private_token
                           for token in tokens}

    news_mrs_rep = get_mrs(repositories_ids, repositories_tokens)
    add_mr_or_start_pipline(session, news_mrs_rep, mrs_ids, sync)
