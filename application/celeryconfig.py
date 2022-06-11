import os

result_backend = os.environ.get('REDIS_LOCATION', 'redis://127.0.0.1:6379/0')
broker_url = os.environ.get('REDIS_LOCATION', 'redis://127.0.0.1:6379/0')
CACHE_BACKEND = 'default'
