import uuid as uuid

from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String, Text,
                        func)
from sqlalchemy.dialects.postgresql import UUID

from application.db.base_class import Base
from conveir.models import PiplineMergeRequests


class Container(Base):
    __tablename__ = "container"

    id = Column(
        String,
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
    )
    status = Column(String, nullable=False)
    name = Column(String, nullable=False)
    image = Column(String, nullable=False)
    command = Column(String, nullable=False)
    created = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())


class ContainerPiplineMergeRequests(Base):
    __tablename__ = "container_pipline_merge_requests"

    id = Column(
        String,
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
    )
    pipline_mr_id = Column(
        UUID(as_uuid=True),
        ForeignKey(PiplineMergeRequests.id, ondelete="CASCADE"),
        nullable=False
    )
    container_id = Column(
        String,
        ForeignKey(Container.id, ondelete="CASCADE"),
        nullable=False
    )
