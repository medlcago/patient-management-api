from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from dtos.health_profile import HealthProfileCreateRequest
    from models import HealthProfile


class HealthProfileServiceInterface(ABC):
    @abstractmethod
    async def create(self, *, data: "HealthProfileCreateRequest") -> "HealthProfile":
        pass

    @abstractmethod
    async def find_all(
            self,
            *options,
            limit: int,
            offset: int,
            order_by: tuple[str, bool] | None = None,
            **kwargs
    ) -> dict[str, int | Sequence["HealthProfile"]]:
        pass

    @abstractmethod
    async def find_health_profile(self, **kwargs) -> "HealthProfile":
        pass
