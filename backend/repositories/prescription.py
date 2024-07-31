from models import Prescription
from repositories.base import SQLAlchemyRepository


class PrescriptionRepository(SQLAlchemyRepository[Prescription]):
    model = Prescription
