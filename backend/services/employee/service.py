from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from dtos.employee import SignUpRequest, EmployeeUpdate
    from core.unitofwork import UnitOfWork
    from models import Employee


class EmployeeService(ABC):
    @abstractmethod
    async def create(self, uow: "UnitOfWork", *, data: "SignUpRequest") -> Optional["Employee"]:
        pass

    @abstractmethod
    async def find_employee(self, uow: "UnitOfWork", **kwargs) -> Optional["Employee"]:
        pass

    @abstractmethod
    async def find_all(
            self, uow: "UnitOfWork",
            *options,
            limit: int,
            offset: int,
            order_by: tuple[str, bool] | None = None,
            **kwargs
    ) -> dict[str, int | Sequence["Employee"]]:
        pass

    @abstractmethod
    async def update(self, uow: "UnitOfWork", *, employee_id: int, data: "EmployeeUpdate") -> Optional["Employee"]:
        pass

    @abstractmethod
    async def update_last_login(self, uow: "UnitOfWork", *, employee_id: int) -> None:
        pass
