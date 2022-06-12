import datetime
import uuid as uuid

from sqlalchemy import Column, DateTime, Enum, ForeignKey, String, func, text
from sqlalchemy.dialects.postgresql import JSONB, UUID

from application.db.base_class import Base
from conveir.const import StatusStageTransporter


class Transporter(Base):
    __tablename__ = "transporter"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
    )
    name = Column(String(255), nullable=True)
    version = Column(String(255), nullable=True)

    extended_pipline = Column(
        JSONB,
        nullable=False,
        server_default=text("'{}'::jsonb")
    )
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())


class StageTransporter(Base):
    __tablename__ = "stage_transporter"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
    )
    transporter_id = Column(
        UUID(as_uuid=True),
        ForeignKey(Transporter.id, ondelete="CASCADE"),
        nullable=False
    )
    start_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
    end_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
    status = Column(Enum(StatusStageTransporter),
                    default=StatusStageTransporter.FUTURE,)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())
