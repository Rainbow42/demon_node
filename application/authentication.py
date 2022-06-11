from typing import Optional
from uuid import UUID

from fastapi import Request
from jose import jwt
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import insert
from starlette.authentication import (AuthCredentials, AuthenticationBackend,
                                      AuthenticationError, BaseUser)
from starlette.responses import JSONResponse

from application import settings
from application.db.session import engine
from users.models import User


class RequestUser(BaseModel):
    keycloak_id: UUID
    email: Optional[str] = None

    class Config:
        orm_mode = True


class KeycloakAuthentication(AuthenticationBackend):
    DEFAULT_AUTHORIZATION_COOKIE_NAME = "Authorization"

    @property
    def authorization_cookie_name(self):
        name = getattr(settings, "AUTHORIZATION_COOKIE_NAME",
                       self.DEFAULT_AUTHORIZATION_COOKIE_NAME)
        return name or self.DEFAULT_AUTHORIZATION_COOKIE_NAME

    async def authenticate(self, request):
        if '/swagger/' in request.url.path \
                or request.url.path.endswith('/openapi.json') \
                or '/internal/' in request.url.path:
            return AuthCredentials(["authenticated"]), BaseUser()
        token = request.headers.get('Authorization') or request.cookies.get(
            self.authorization_cookie_name)
        if not token:
            raise AuthenticationError('No Authorization token in request!')
        try:
            data = jwt.decode(
                token[7:] if token.startswith('Bearer') else token,
                key=settings.JWT_PUB_KEY, audience=settings.KEYCLOAK_AUDIENCE
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationError('Token signature has expired')
        except jwt.JWTError:
            raise AuthenticationError('Invalid token')

        user_token = dict(
            id=data.get('sub'),
            last_name=data.get('family_name'),
            first_name=data.get('given_name'),
            patronymic=data.get('patronymic')
        )
        insert_users = insert(User).values(**user_token)
        do_update_users = insert_users.on_conflict_do_update(
            index_elements=[User.id],
            set_=user_token
        )

        async with engine.begin() as db_session:
            await db_session.execute(do_update_users)
        request_user = RequestUser(keycloak_id=data.get('sub'),
                                   email=data.get("email", ""))
        return AuthCredentials(["user"]), request_user


def error(request: Request, exc: Exception):
    return JSONResponse({"detail": str(exc)}, status_code=401)
