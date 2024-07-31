from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.mixins import IntIdPkMixin

if TYPE_CHECKING:
    from models.patient import Patient
    from models.prescription import Prescription
    from models.employee import Employee


class MedicalRecord(IntIdPkMixin, Base):
    """
    A model for storing records of patient medical visits
    """
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"))
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))
    visit_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    diagnosis: Mapped[str]
    treatment: Mapped[str]
    notes: Mapped[str]

    patient: Mapped["Patient"] = relationship(back_populates="medical_records")
    employee: Mapped["Employee"] = relationship(back_populates="medical_records")
    prescription: Mapped["Prescription"] = relationship(back_populates="medical_record", lazy="joined", cascade="all, delete, delete-orphan")
