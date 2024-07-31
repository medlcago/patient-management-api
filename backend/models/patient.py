from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from models.base import Base
from models.mixins import IntIdPkMixin, CreatedAtMixin

if TYPE_CHECKING:
    from models.medical_record import MedicalRecord
    from models.health_profile import HealthProfile


class Patient(IntIdPkMixin, CreatedAtMixin, Base):
    """
    A model for storing patient information
    """
    full_name: Mapped[str]
    date_of_birth: Mapped[date]
    gender: Mapped[str]
    address: Mapped[str]
    email: Mapped[str | None]
    phone_number: Mapped[str | None]

    health_profile: Mapped["HealthProfile"] = relationship(back_populates="patient", cascade="all, delete, delete-orphan")
    medical_records: Mapped[list["MedicalRecord"]] = relationship(back_populates="patient", cascade="all, delete, delete-orphan")
