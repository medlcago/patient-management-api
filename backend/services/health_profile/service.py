from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from dtos.health_profile import HealthProfileCreateRequest
    from core.unitofwork import UnitOfWork
    from models import HealthProfile


class HealthProfileService(ABC):
    @abstractmethod
    async def create(self, uow: "UnitOfWork", *, data: "HealthProfileCreateRequest") -> "HealthProfile":
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
    ) -> dict[str, int | Sequence["HealthProfile"]]:
        pass

    @abstractmethod
    async def find_health_profile(self, uow: "UnitOfWork", **kwargs) -> "HealthProfile":
        pass
