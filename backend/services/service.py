from core.unitofwork import UnitOfWork

from services.auth import AuthService
from services.employee import EmployeeService
from services.health_profile import HealthProfileService
from services.medical_record import MedicalRecordService
from services.patient import PatientService
from services.prescription import PrescriptionService


class Service:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def __call__(self):
        self.employee_service = EmployeeService(uow=self.uow)
        self.auth_service = AuthService(employee_service=self.employee_service)
        self.health_profile_service = HealthProfileService(uow=self.uow)
        self.medical_record_service = MedicalRecordService(uow=self.uow)
        self.patient_service = PatientService(uow=self.uow)
        self.prescription_service = PrescriptionService(uow=self.uow)
        return self
