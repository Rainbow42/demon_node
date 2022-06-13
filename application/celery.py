import logging

from celery import Celery

log = logging.getLogger('demon_node')

app = Celery('demon_node')

app.config_from_object('application.celeryconfig')

app.conf.timezone = 'UTC'

app.conf.imports = [
    'tasks.tasks',
]

app.conf.beat_schedule = {
    'check_update_merge_request': {
        'task': 'tasks.tasks.check_update_merge_request',
        'schedule': 3.0,
        # 'args': (16, 16)
    },
}
