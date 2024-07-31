from models import MedicalRecord
from repositories.base import SQLAlchemyRepository


class MedicalRecordRepository(SQLAlchemyRepository[MedicalRecord]):
    model = MedicalRecord
