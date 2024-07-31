from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from models.base import Base
from models.mixins import IntIdPkMixin

if TYPE_CHECKING:
    from models.medical_record import MedicalRecord


class Prescription(IntIdPkMixin, Base):
    """
    A model for storing information about a patient's prescribed medications
    """
    medical_record_id: Mapped[int] = mapped_column(ForeignKey("medical_records.id"))
    medication_name: Mapped[str]
    dosage: Mapped[str]
    start_date: Mapped[date]
    end_date: Mapped[date]

    medical_record: Mapped["MedicalRecord"] = relationship(back_populates="prescription")

    __table__args__ = (UniqueConstraint("medical_record_id"),)
