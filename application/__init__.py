import os.path
import sys

from .celery import app as celery_app

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

__all__ = ("celery_app",)
