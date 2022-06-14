import asyncio
import logging

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert

from application.celery import app
from application.db.session import SessionLocal
from conveir.const import StatusStageTransporter
from conveir.models import TransporterRepositories, Transporter, \
    StageTransporter, PiplineMergeRequests
from helpers.gitlab import GitlabHelpersNoRequest
from pipeline.containers import RunPipline
from repositories.models import Repositories, MergeRequest, RepositoriesToken, \
    RepositoriesUsers

logger = logging.getLogger(__name__)


@app.task(shared=True)
def pipelines_run(mr_id, rep_id):
    logger.info("START PIPELINES")
    loop = asyncio.get_event_loop()
    sync = loop.run_until_complete

    session = SessionLocal()
    query_rep = select(Repositories.id).where(
        Repositories.id_repositories == rep_id)
    repositories = sync(session.execute(query_rep)).scalars().first()

    query_trans = (
        select(TransporterRepositories,
               Transporter.extended_pipline,
               Transporter.id.label('tr_id')).
            join(Transporter).
            where(TransporterRepositories.repositories_id == repositories)
    )
    trans = sync(session.execute(query_trans)).fetchone()

    query_pmr = select(PiplineMergeRequests.id,
                       PiplineMergeRequests.status,
                       PiplineMergeRequests.stage_transporter_id).where(
        PiplineMergeRequests.mr_id == mr_id,
        PiplineMergeRequests.stage_transporter_id == None
    )

    pmr = sync(session.execute(query_pmr)).fetchone()
    query_pmr_up = update(PiplineMergeRequests).where(
        PiplineMergeRequests.id == pmr.id
    ).values({'status': StatusStageTransporter.PROGRESS.value})
    sync(session.execute(query_pmr_up))

    sync(session.commit())

    stage_tr = StageTransporter(transporter_id=trans.tr_id)
    session.add(stage_tr)
    sync(session.flush())

    query_pmr_up = update(PiplineMergeRequests).where(
        PiplineMergeRequests.id == pmr.id
    ).values({'stage_transporter_id':stage_tr.id})
    sync(session.execute(query_pmr_up))
    sync(session.commit())

    for stage in trans.extended_pipline:
        stage_tr.stage = stage
        logger.info(f"PIPELINES MR id {mr_id} stage {stage}")
        sync(session.flush())
        result: bool = RunPipline().run(stage)
        if not result:
            query_pmr_up = update(PiplineMergeRequests).where(
                PiplineMergeRequests.id == pmr.id
            ).values({'status': StatusStageTransporter.FAILED.value})
            sync(session.execute(query_pmr_up))
            sync(session.commit())
            logger.info(f"PIPELINES MR id {mr_id} stage {pmr.status}")
            return

    query_pmr_up = update(PiplineMergeRequests).where(
        PiplineMergeRequests.id == pmr.id
    ).values({'status': StatusStageTransporter.DONE.value})
    sync(session.execute(query_pmr_up))

    sync(session.commit())
    return


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


def add_mr(new_mr, sync, session, rep_id):
    author = new_mr.author.dict()
    new_mr = new_mr.dict(exclude_unset=True, exclude={"author"})
    new_mr["author_id"] = author.get("id")

    query = select(Repositories.id).where(
        Repositories.id_repositories == rep_id)
    repositories = sync(session.execute(query)).scalars().first()

    new_mr["repositories_id"] = repositories
    insert_mr = insert(MergeRequest).values(**new_mr)
    do_update_pmr = insert_mr.on_conflict_do_update(
        index_elements=[MergeRequest.id],
        set_=new_mr
    )
    sync(session.execute(do_update_pmr))


def add_pipline_mr(new_mr, sync, session):
    pipline_mr = dict(mr_id=new_mr.id,
                      status=StatusStageTransporter.FUTURE)
    insert_mr = insert(PiplineMergeRequests).values(**pipline_mr)
    do_update_pmr = insert_mr.on_conflict_do_update(
        index_elements=[PiplineMergeRequests.id],
        set_=pipline_mr
    )
    sync(session.execute(do_update_pmr))
    sync(session.flush())


def add_mr_or_start_pipline(session: SessionLocal,
                            news_mrs_rep: dict,
                            mrs_ids: dict,
                            sync):
    for rep_id, new_mrs in news_mrs_rep.items():
        for new_mr in new_mrs:
            old_mr = mrs_ids.get(new_mr.id)
            if old_mr and new_mr.updated_at > old_mr.updated_at \
                    and new_mr.state == 'opened':
                add_mr(new_mr, sync, session, rep_id)
                add_pipline_mr(old_mr, sync, session)
                pipelines_run.delay(old_mr.id, rep_id)
            elif not old_mr:
                add_mr(new_mr, sync, session, rep_id)
                add_pipline_mr(new_mr, sync, session)
                pipelines_run.delay(new_mr.id, rep_id)

            sync(session.flush())
            author = new_mr.author.dict()
            insert_mr = insert(RepositoriesUsers).values(**author)
            do_update_pmr = insert_mr.on_conflict_do_update(
                index_elements=[RepositoriesUsers.id],
                set_=author
            )
            sync(session.execute(do_update_pmr))
            sync(session.flush())

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
