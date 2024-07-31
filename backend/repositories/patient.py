from models import Patient
from repositories.base import SQLAlchemyRepository


class PatientRepository(SQLAlchemyRepository[Patient]):
    model = Patient
