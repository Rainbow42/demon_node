import logging

from celery import Celery

from application import settings

log = logging.getLogger('demon_node')

app = Celery('demon_node')

app.config_from_object('application.celeryconfig')

app.conf.timezone = 'UTC'

app.conf.imports = [
    'tasks.tasks',
]
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'check_update_merge_request': {
        'task': 'tasks.tasks.check_update_merge_request',
        'schedule': settings.CHECK_MR_TIME_TASKS,
        # 'args': (16, 16)
    },
}
