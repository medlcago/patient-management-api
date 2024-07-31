from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from dtos.mixins import AtLeastOneFieldNotNoneMixin
from enums.employee import EmployeeRole


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str
    role: EmployeeRole


class EmployeeResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: EmployeeRole
    is_active: bool
    created_date: datetime
    last_login: datetime | None


class EmployeeUpdate(AtLeastOneFieldNotNoneMixin, BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    role: EmployeeRole | None = None
    is_active: bool | None = None
