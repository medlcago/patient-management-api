from pydantic import BaseModel

from dtos.patient import PatientResponse
from enums.patient import BloodType


class HealthProfileCreateRequest(BaseModel):
    patient_id: int
    height: float
    weight: float
    blood_type: BloodType
    allergies: str | None = None
    chronic_conditions: str | None = None


class HealthProfileCreateResponse(HealthProfileCreateRequest):
    id: int


class HealthProfileResponse(HealthProfileCreateResponse):
    patient: PatientResponse

