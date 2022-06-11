# import logging
#
# from celery import Celery
# from notify_service.utils import load_notifications
#
# log = logging.getLogger('async-survey')
#
# app = Celery('async-survey')
#
# app.config_from_object('application.celeryconfig')
#
# app.conf.timezone = 'UTC'
#
# load_notifications()
#
# app.autodiscover_tasks(['sendings'], 'tasks')
