import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_file_path = os.path.join(BASE_DIR, '.env')


SERVER_HOST = os.getenv('SERVER_HOST', 'localhost')
SERVER_PORT = int(os.getenv('SERVER_PORT', 8000))

DB_NAME = os.getenv('DB_NAME', 'intranet')
DB_USER = os.getenv('DB_USER', 'intranet')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')

LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
DEBUG = os.getenv('DEBUG', 1) in [1, '1', True, 'True', 'true']
DEBUG_TOOLBAR_ENABLED = os.getenv('DEBUG_TOOLBAR_ENABLED', 0) in [1, '1', True, 'True', 'true']
BASE_API_URL = os.getenv('BASE_API_URL', '/api/demon').rstrip('/')

log_level = getattr(logging, LOG_LEVEL, logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(levelname)s [%(asctime)s] %(name)s: %(message)s', '%d-%m-%Y %H:%M:%S'))

logger = logging.getLogger("async-demon")
logger.setLevel(log_level)
logger.addHandler(handler)
handler.setLevel(log_level)


POOL_SIZE = int(os.getenv('POOL_SIZE', 600))
POOL_RECYCLE = int(os.getenv('POOL_RECYCLE', 3600))
POOL_TIMEOUT = int(os.getenv('POOL_TIMEOUT', 100))
MAX_OVERFLOW = int(os.getenv('MAX_OVERFLOW', 100))

GITLAB_API_URL = os.getenv('GITLAB_API_URL', 'https://gitlab.com/').rstrip('/')


class GITLAB_API:
    get_detail_repositories = GITLAB_API_URL + '/api/v4/projects/{}/'
    get_merge_requests = GITLAB_API_URL + '/api/v4/projects/{}/merge_requests/'
    get_users = GITLAB_API_URL + '/api/v4/projects/{}/users/'