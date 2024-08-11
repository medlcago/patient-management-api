from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dtos.prescription import PrescriptionCreateRequest
    from models import Prescription


class PrescriptionServiceInterface(ABC):
    @abstractmethod
    async def create(self, *, data: "PrescriptionCreateRequest") -> "Prescription":
        pass

    @abstractmethod
    async def find_prescription(self, **kwargs) -> "Prescription":
        pass

    @abstractmethod
    async def delete_prescription(self, **kwargs) -> None:
        pass
