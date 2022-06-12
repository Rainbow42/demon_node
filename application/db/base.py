# Import all the models, so that Base has them before being
# imported by Alembic
# НУЖНО СОХРАНЯТЬ ПОРЯДОК ЗАВИСИМОСТЕЙ, ТАК КАК ЭТО ОЧЕРЕДНОСТЬ СОЗДАНИЯ МИГРАЦИЙ
# СОРТИРОВКИ НЕ ПРИМЕНЯТЬ

from application.db.base_class import Base  # noqa
from conveir.models import StageTransporter  # noqa
from conveir.models import Transporter  # noqa
from repositories.models import Repositories  # noqa
from repositories.models import Repositories  # noqa
from repositories.models import RepositoriesUsers  # noqa
from repositories.models import RepositoriesToken  # noqa
from conveir.models import PiplineMergeRequests  # noqa
from conveir.models import TransporterRepositories  # noqa
