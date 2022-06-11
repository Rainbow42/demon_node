from enum import Enum


class StatusStageTransporter(Enum):
    FAILED = 'FAILED'
    DONE = 'DONE'
    PROGRESS = 'PROGRESS'
    FUTURE = 'FUTURE'
