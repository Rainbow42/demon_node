from enum import Enum


class StatusStageTransporter(Enum):
    FAILED = 'FAILED'
    DONE = 'DONE'
    PROGRESS = 'PROGRESS'
    FUTURE = 'FUTURE'


class PipelinesEnum(str, Enum):
    BUILD = 'BUILD'
    TESTING = 'TESTING'
    LINTERS = 'LINTERS'
    INSTALLATION = 'INSTALLATION'
