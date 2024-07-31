from fastapi import APIRouter, Depends, Query

from api.deps import UOWDep, currentActiveEmployeeDep, require_roles
from dtos.employee import SignUpRequest, EmployeeResponse, EmployeeUpdate
from dtos.pagination import PaginationResponse
from enums.employee import admin_only
from services import employee_service

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post("/", response_model=EmployeeResponse, status_code=201, dependencies=[Depends(require_roles(*admin_only))])
async def register_employee(uow: UOWDep, data: SignUpRequest):
    employee = await employee_service.create(uow, data=data)
    return employee


@router.get("/me/", response_model=EmployeeResponse)
async def me(employee: currentActiveEmployeeDep):
    return employee


@router.get("/{employee_id}/", response_model=EmployeeResponse, dependencies=[Depends(require_roles(*admin_only))])
async def find_employee_by_id(employee_id: int, uow: UOWDep):
    employee = await employee_service.find_employee(uow, id=employee_id)
    return employee


@router.get("/", response_model=PaginationResponse[EmployeeResponse], dependencies=[Depends(require_roles(*admin_only))])
async def find_all_employees(
        uow: UOWDep,
        limit: int = Query(default=10, ge=0),
        offset: int = Query(default=0, ge=0),
        is_active: bool = Query(default=True)
):
    employees = await employee_service.find_all(uow, limit=limit, offset=offset, is_active=is_active)
    return employees


@router.patch("/{employee_id}/", response_model=EmployeeResponse, dependencies=[Depends(require_roles(*admin_only))])
async def update_employee(employee_id: int, uow: UOWDep, data: EmployeeUpdate):
    employee = await employee_service.update(uow, employee_id=employee_id, data=data)
    return employee
