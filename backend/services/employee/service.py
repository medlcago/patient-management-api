from typing import TYPE_CHECKING, Sequence

from fastapi import HTTPException

from core import security
from services.employee.interface import EmployeeServiceInterface
from utils.time import get_current_utc_time

if TYPE_CHECKING:
    from dtos.employee import SignUpRequest, EmployeeUpdate
    from core.unitofwork import UnitOfWork
    from models import Employee


class EmployeeService(EmployeeServiceInterface):
    def __init__(self, uow: "UnitOfWork"):
        self.uow = uow

    async def create(self, *, data: "SignUpRequest") -> "Employee":
        async with self.uow:
            if await self.uow.employee.filter(email=data.email):
                raise HTTPException(
                    status_code=409,
                    detail="Employee already exists",
                )
            data.password = security.hash_password(data.password)
            employee = await self.uow.employee.create(**data.model_dump())
            return employee

    async def find_employee(self, **kwargs) -> "Employee":
        async with self.uow:
            employee = await self.uow.employee.filter(**kwargs)
            if not employee:
                raise HTTPException(
                    status_code=404,
                    detail="Employee not found"
                )
            return employee

    async def find_all(
            self,
            *options,
            limit: int,
            offset: int,
            order_by: tuple[str, bool] | None = None,
            **kwargs
    ) -> dict[str, int | Sequence["Employee"]]:
        async with self.uow:
            employees = await self.uow.employee.find_all(
                limit=limit,
                offset=offset,
                order_by=order_by,
                *options,
                **kwargs
            )
            return employees

    async def update(self, *, employee_id: int, data: "EmployeeUpdate") -> "Employee":
        async with self.uow:
            employee = await self.uow.employee.update(employee_id, **data.model_dump(exclude_none=True))
            if not employee:
                raise HTTPException(
                    status_code=404,
                    detail="Employee not found"
                )
            return employee

    async def update_last_login(self, *, employee_id: int) -> None:
        async with self.uow:
            await self.uow.employee.update(employee_id, last_login=get_current_utc_time())
