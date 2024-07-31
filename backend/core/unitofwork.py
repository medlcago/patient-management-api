from core.db import db_helper
from repositories import EmployeeRepository
from repositories import HealthProfileRepository
from repositories import MedicalRecordRepository
from repositories import PatientRepository
from repositories import PrescriptionRepository


class UnitOfWork:
    def __init__(self):
        self.session_factory = db_helper.session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.employee = EmployeeRepository(self.session)
        self.patient = PatientRepository(self.session)
        self.health_profile = HealthProfileRepository(self.session)
        self.medical_record = MedicalRecordRepository(self.session)
        self.prescription = PrescriptionRepository(self.session)

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()
        await self.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def close(self):
        await self.session.close()
