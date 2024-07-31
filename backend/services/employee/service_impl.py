from typing import TYPE_CHECKING, Sequence

from fastapi import HTTPException

from core import security
from services.employee.service import EmployeeService
from utils.time import get_current_utc_time

if TYPE_CHECKING:
    from dtos.employee import SignUpRequest, EmployeeUpdate
    from core.unitofwork import UnitOfWork
    from models import Employee


class EmployeeServiceImpl(EmployeeService):
    async def create(self, uow: "UnitOfWork", *, data: "SignUpRequest") -> "Employee":
        async with uow:
            if await uow.employee.filter(email=data.email):
                raise HTTPException(
                    status_code=409,
                    detail="Employee already exists",
                )
            data.password = security.hash_password(data.password)
            employee = await uow.employee.create(**data.model_dump())
            return employee

    async def find_employee(self, uow: "UnitOfWork", **kwargs) -> "Employee":
        async with uow:
            employee = await uow.employee.filter(**kwargs)
            if not employee:
                raise HTTPException(
                    status_code=404,
                    detail="Employee not found"
                )
            return employee

    async def find_all(
            self,
            uow: "UnitOfWork",
            *options,
            limit: int,
            offset: int,
            order_by: tuple[str, bool] | None = None,
            **kwargs
    ) -> dict[str, int | Sequence["Employee"]]:
        async with uow:
            employees = await uow.employee.find_all(limit=limit, offset=offset, order_by=order_by, *options, **kwargs)
            return employees

    async def update(self, uow: "UnitOfWork", *, employee_id: int, data: "EmployeeUpdate") -> "Employee":
        async with uow:
            employee = await uow.employee.update(employee_id, **data.model_dump(exclude_none=True))
            if not employee:
                raise HTTPException(
                    status_code=404,
                    detail="Employee not found"
                )
            return employee

    async def update_last_login(self, uow: "UnitOfWork", *, employee_id: int) -> None:
        async with uow:
            await uow.employee.update(employee_id, last_login=get_current_utc_time())


employee_service = EmployeeServiceImpl()
