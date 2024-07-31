from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Sequence, Optional

if TYPE_CHECKING:
    from dtos.patient import PatientCreateRequest
    from dtos.patient import PatientUpdate
    from core.unitofwork import UnitOfWork
    from models import Patient


class PatientService(ABC):
    @abstractmethod
    async def create(self, uow: "UnitOfWork", *, data: "PatientCreateRequest") -> "Patient":
        pass

    @abstractmethod
    async def find_all(
            self,
            uow: "UnitOfWork",
            *options,
            limit: int,
            offset: int,
            order_by: tuple[str, bool] | None = None,
            **kwargs
    ) -> dict[str, int | Sequence["Patient"]]:
        pass

    @abstractmethod
    async def find_patient(self, uow: "UnitOfWork", **kwargs) -> Optional["Patient"]:
        pass

    @abstractmethod
    async def update(self, uow: "UnitOfWork", *, patient_id: int, data: "PatientUpdate") -> Optional["Patient"]:
        pass
