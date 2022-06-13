import logging
from typing import List, Union

import ujson
from aiohttp import ClientSession, TCPConnector
from fastapi import HTTPException, Request

from application import settings
from application.settings import handler, log_level
from helpers.schemas import MergeRequestBase, RepositoriesBase, UsersBase

logger = logging.getLogger("GitLab")
logger.setLevel(log_level)
logger.addHandler(handler)
handler.setLevel(log_level)


class GitLabHelpersBase:
    helpers = None
    project_id = None

    async def get_detail_repositories(self) -> RepositoriesBase:
        url = settings.GITLAB_API.get_detail_repositories.format(
            self.project_id)
        text = await self.send_request(url)
        repositories = ujson.loads(text)
        return RepositoriesBase(
            id=repositories.get("id"),
            description=repositories.get("description"),
            name=repositories.get("name"),
            created_at=repositories.get("created_at")
        )

    async def get_merge_requests(self, query: list = None) -> List[MergeRequestBase]:
        if query is None:
            query = list()
            query.append([("state", "opened")])

        url = settings.GITLAB_API.get_merge_requests.format(self.project_id)
        text = await self.send_request(url)
        items = ujson.loads(text)
        return [MergeRequestBase(**mr) for mr in items]

    async def send_request(self, url) -> str:
        print(self.helpers)
        async with ClientSession(
                connector=TCPConnector(verify_ssl=False), **self.helpers
        ) as session:
            logger.debug(f"GET {url}")
            async with session.get(url) as response:
                text = await response.text()
                logger.debug(f"response {text}")
                if response.status != 200:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Ошибка при получение информации о списке МР"
                    )
                return text

    async def get_users(self, to_dict: bool = False) -> Union[
        dict, List[UsersBase]]:
        url = settings.GITLAB_API.get_users.format(self.project_id)
        text = await self.send_request(url)
        users = ujson.loads(text)
        if to_dict:
            return {
                user.get("id"):
                    UsersBase(
                        id=user.get("id"),
                        username=user.get("username"),
                        name=user.get("name")
                    )
                for user in users
            }

        return [
            UsersBase(
                id=user.get("id"),
                username=user.get("username"),
                name=user.get("name")
            ) for user in users]


class GitlabHelpersNoRequest(GitLabHelpersBase):
    def __init__(self,  private_token: str, project_id: int,):
        self.helpers = {
            'headers': {
                'Content-Type':'application/json',
                'PRIVATE-TOKEN': private_token
            },
        }
        self.project_id = project_id


class GitLabHelpers(GitLabHelpersBase):
    def __init__(self, request: Request, private_token: str, project_id: int, helpers:dict = None):

        self.helpers = {
            'cookies': request.cookies,
            'headers': {
                'Content-Type': request.headers.get('Content-Type',
                                                    'application/json'),
                'Authorization': request.headers.get('Authorization', ''),
                'PRIVATE-TOKEN': private_token
            },
        }
        self.project_id = project_id

