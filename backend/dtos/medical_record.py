from datetime import datetime

from pydantic import BaseModel

from dtos.prescription import PrescriptionResponse


class MedicalRecordCreateRequest(BaseModel):
    patient_id: int
    visit_date: datetime
    diagnosis: str
    treatment: str
    notes: str


class MedicalRecordCreateResponse(MedicalRecordCreateRequest):
    id: int
    employee_id: int


class MedicalRecordResponse(MedicalRecordCreateResponse):
    prescription: PrescriptionResponse | None
