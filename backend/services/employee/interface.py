from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from dtos.employee import SignUpRequest, EmployeeUpdate
    from models import Employee


class EmployeeServiceInterface(ABC):
    @abstractmethod
    async def create(self, *, data: "SignUpRequest") -> "Employee":
        pass

    @abstractmethod
    async def find_employee(self, **kwargs) -> "Employee":
        pass

    @abstractmethod
    async def find_all(
            self,
            *options,
            limit: int,
            offset: int,
            order_by: tuple[str, bool] | None = None,
            **kwargs
    ) -> dict[str, int | Sequence["Employee"]]:
        pass

    @abstractmethod
    async def update(self, *, employee_id: int, data: "EmployeeUpdate") -> "Employee":
        pass

    @abstractmethod
    async def update_last_login(self, *, employee_id: int) -> None:
        pass
