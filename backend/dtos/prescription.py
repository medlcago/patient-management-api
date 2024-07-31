from datetime import date

from pydantic import BaseModel


class PrescriptionCreateRequest(BaseModel):
    medical_record_id: int
    medication_name: str
    dosage: str
    start_date: date
    end_date: date


class PrescriptionCreateResponse(PrescriptionCreateRequest):
    id: int


class PrescriptionResponse(PrescriptionCreateResponse):
    pass
