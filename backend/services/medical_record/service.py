from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from core.unitofwork import UnitOfWork
    from dtos.medical_record import MedicalRecordCreateRequest
    from models import MedicalRecord


class MedicalRecordService(ABC):
    @abstractmethod
    async def create(
            self,
            uow: "UnitOfWork",
            *,
            employee_id: int,
            data: "MedicalRecordCreateRequest"
    ) -> "MedicalRecord":
        pass

    @abstractmethod
    async def find_all(
            self, uow: "UnitOfWork",
            *options,
            limit: int,
            offset: int,
            order_by: tuple[str, bool] | None = None,
            **kwargs
    ) -> dict[str, int | Sequence["MedicalRecord"]]:
        pass

    @abstractmethod
    async def find_medical_record(self, uow: "UnitOfWork", **kwargs) -> "MedicalRecord":
        pass
