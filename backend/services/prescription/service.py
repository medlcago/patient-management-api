from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from core.unitofwork import UnitOfWork
    from dtos.prescription import PrescriptionCreateRequest
    from models import Prescription


class PrescriptionService(ABC):
    @abstractmethod
    async def create(self, uow: "UnitOfWork", *, data: "PrescriptionCreateRequest") -> Optional["Prescription"]:
        pass

    @abstractmethod
    async def find_prescription(self, uow: "UnitOfWork", **kwargs) -> Optional["Prescription"]:
        pass

    @abstractmethod
    async def delete_prescription(self, uow: "UnitOfWork", **kwargs) -> None:
        pass
