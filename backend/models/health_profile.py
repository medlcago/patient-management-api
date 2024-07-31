from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.mixins import IntIdPkMixin, CreatedAtMixin

if TYPE_CHECKING:
    from models.patient import Patient


class HealthProfile(IntIdPkMixin, CreatedAtMixin, Base):
    """
    A model for storing patient health information
    """
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"))
    height: Mapped[float]
    weight: Mapped[float]
    blood_type: Mapped[str]
    allergies: Mapped[str] = mapped_column(default="-")
    chronic_conditions: Mapped[str] = mapped_column(default="-")

    patient: Mapped["Patient"] = relationship(back_populates="health_profile", lazy="joined")

    __table_args__ = (UniqueConstraint("patient_id"),)
