from datetime import date

from pydantic import BaseModel, EmailStr

from dtos.mixins import AtLeastOneFieldNotNoneMixin
from enums.patient import Gender


class PatientCreateRequest(BaseModel):
    full_name: str
    date_of_birth: date
    gender: Gender
    address: str
    email: EmailStr | None = None
    phone_number: str | None = None


class PatientCreateResponse(PatientCreateRequest):
    id: int


class PatientResponse(PatientCreateResponse):
    pass


class PatientUpdate(AtLeastOneFieldNotNoneMixin, BaseModel):
    full_name: str | None = None
    date_of_birth: date | None = None
    gender: Gender | None = None
    address: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
