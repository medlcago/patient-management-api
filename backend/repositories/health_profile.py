from models import HealthProfile
from repositories.base import SQLAlchemyRepository


class HealthProfileRepository(SQLAlchemyRepository[HealthProfile]):
    model = HealthProfile
