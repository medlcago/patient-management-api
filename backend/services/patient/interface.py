from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from dtos.patient import PatientCreateRequest
    from dtos.patient import PatientUpdate
    from models import Patient


class PatientServiceInterface(ABC):
    @abstractmethod
    async def create(self, *, data: "PatientCreateRequest") -> "Patient":
        pass

    @abstractmethod
    async def find_all(
            self,
            *options,
            limit: int,
            offset: int,
            order_by: tuple[str, bool] | None = None,
            **kwargs
    ) -> dict[str, int | Sequence["Patient"]]:
        pass

    @abstractmethod
    async def find_patient(self, **kwargs) -> "Patient":
        pass

    @abstractmethod
    async def update(self, *, patient_id: int, data: "PatientUpdate") -> "Patient":
        pass
