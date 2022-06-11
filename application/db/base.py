# Import all the models, so that Base has them before being
# imported by Alembic
# НУЖНО СОХРАНЯТЬ ПОРЯДОК ЗАВИСИМОСТЕЙ, ТАК КАК ЭТО ОЧЕРЕДНОСТЬ СОЗДАНИЯ МИГРАЦИЙ
# СОРТИРОВКИ НЕ ПРИМЕНЯТЬ

from application.db.base_class import Base  # noqa
from conveir.models import Transporter  # noqa
from conveir.models import StageTransporter  # noqa


