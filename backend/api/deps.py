from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from core.security import decode_token
from core.unitofwork import UnitOfWork
from enums.employee import EmployeeRole
from models import Employee
from services import Service

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"api/v1/auth/token"
)

UOWDep = Annotated[UnitOfWork, Depends()]

ServiceDep = Annotated[Service, Depends(Service(uow=UnitOfWork()))]

TokenDep = Annotated[str, Depends(oauth2_scheme)]


async def current_employee(service: ServiceDep, token: TokenDep) -> Employee:
    exp401 = HTTPException(
        status_code=401,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"}
    )
    payload = decode_token(token)
    if not payload:
        raise exp401

    token_type = payload.get("token_type")
    if token_type != "access":
        raise exp401
    employee_id = payload.get("employee_id")
    employee = await service.employee_service.find_employee(id=employee_id)
    if not employee:
        raise exp401
    return employee


currentEmployeeDep = Annotated[Employee, Depends(current_employee)]


async def current_active_employee(employee: currentEmployeeDep) -> Employee:
    if not employee.is_active:
        raise HTTPException(
            status_code=403,
            detail="Inactive"
        )
    return employee


currentActiveEmployeeDep = Annotated[Employee, Depends(current_active_employee)]


def require_roles(*required_roles: EmployeeRole):
    async def check_roles(employee: currentActiveEmployeeDep):
        if employee.role not in required_roles:
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )
        return employee

    return check_roles
