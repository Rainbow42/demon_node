import uuid as uuid

from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String, Text,
                        func)
from sqlalchemy.dialects.postgresql import UUID

from application.db.base_class import Base


class Repositories(Base):
    __tablename__ = "repositories"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
    )
    id_repositories = Column(
        Integer,
        nullable=False,
        unique=True
    )
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())


class RepositoriesUsers(Base):
    __tablename__ = "repositories_users"
    id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        unique=True
    )
    username = Column(String, nullable=False)
    name = Column(String, nullable=False)


class RepositoriesToken(Base):
    """Отдельная сущность для токенов,
     так как они могут быть с разными правами доступа"""

    __tablename__ = "repositories_token"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
    )
    user_id = Column(
        Integer,
        ForeignKey(RepositoriesUsers.id, ondelete="CASCADE"),
        nullable=False
    )
    repositories_id = Column(
        UUID(as_uuid=True),
        ForeignKey(Repositories.id, ondelete="CASCADE"),
        nullable=False
    )
    private_token = Column(
        String,
        nullable=False,
        unique=True
    )


class MergeRequest(Base):
    __tablename__ = "merge_request"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
    )
    author_id = Column(
        Integer,
        ForeignKey(RepositoriesUsers.id, ondelete="CASCADE"),
        nullable=False
    )
    repositories_id = Column(
        UUID(as_uuid=True),
        ForeignKey(Repositories.id, ondelete="CASCADE"),
        nullable=False
    )
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    state = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())
    target_branch = Column(String, nullable=False)
    source_branch = Column(String, nullable=False)
