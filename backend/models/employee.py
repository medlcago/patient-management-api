from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.mixins import IntIdPkMixin, CreatedAtMixin

if TYPE_CHECKING:
    from models.medical_record import MedicalRecord


class Employee(IntIdPkMixin, CreatedAtMixin, Base):
    """
    A model for storing employee information
    """
    email: Mapped[str] = mapped_column(unique=True)
    full_name: Mapped[str]
    role: Mapped[str]
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    last_login: Mapped[datetime | None]

    medical_records: Mapped[list["MedicalRecord"]] = relationship(back_populates="employee", cascade="all, delete, delete-orphan")
