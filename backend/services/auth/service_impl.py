from typing import TYPE_CHECKING, Optional

from fastapi import HTTPException

from core import security
from core.security import verify_password
from dtos.auth import Token, AccessToken
from services.auth.service import AuthService
from services.employee.service_impl import employee_service

if TYPE_CHECKING:
    from core.unitofwork import UnitOfWork
    from models import Employee


class AuthServiceImpl(AuthService):
    async def login(self, uow: "UnitOfWork", *, username: str, password: str) -> Token:
        employee = await self.authenticate(uow, username=username, password=password)

        access = security.access_token(employee_id=employee.id)
        refresh = security.refresh_token(employee_id=employee.id)

        await employee_service.update_last_login(uow, employee_id=employee.id)
        return Token(
            access_token=access,
            refresh_token=refresh
        )

    async def refresh_token(self, token: str) -> Optional[AccessToken]:
        exp401 = HTTPException(
            status_code=401,
            detail="Invalid token"
        )

        token = security.decode_token(token=token)
        if not token:
            raise exp401
        token_type = token.get("token_type")
        if token_type != "refresh":
            raise exp401

        employee_id = token.get("employee_id")
        access = security.access_token(employee_id=employee_id)
        return AccessToken(
            access_token=access
        )

    async def authenticate(self, uow: "UnitOfWork", *, username: str, password: str) -> "Employee":
        employee = await employee_service.find_employee(uow, email=username)
        if not employee or not verify_password(password, employee.password):
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password"
            )
        if not employee.is_active:
            raise HTTPException(
                status_code=403,
                detail="Inactive",
            )
        return employee


auth_service = AuthServiceImpl()
