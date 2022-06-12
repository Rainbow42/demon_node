import logging

from celery import Celery

log = logging.getLogger('demon_node')

app = Celery('demon_node')

app.config_from_object('application.celeryconfig')

app.conf.timezone = 'UTC'


app.autodiscover_tasks(['pipeline.tasks'])

