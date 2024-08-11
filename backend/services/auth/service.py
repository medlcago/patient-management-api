from typing import TYPE_CHECKING

from fastapi import HTTPException

from core import security
from core.security import verify_password
from dtos.auth import Token, AccessToken
from services.auth.interface import AuthServiceInterface

if TYPE_CHECKING:
    from models import Employee
    from services.employee.interface import EmployeeServiceInterface


class AuthService(AuthServiceInterface):
    def __init__(self, employee_service: "EmployeeServiceInterface") -> None:
        self.employee_service = employee_service

    async def login(self, *, username: str, password: str) -> Token:
        employee = await self.authenticate(username=username, password=password)

        access = security.access_token(employee_id=employee.id)
        refresh = security.refresh_token(employee_id=employee.id)

        await self.employee_service.update_last_login(employee_id=employee.id)
        return Token(
            access_token=access,
            refresh_token=refresh
        )

    async def refresh_token(self, *, token: str) -> AccessToken:
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

    async def authenticate(self, *, username: str, password: str) -> "Employee":
        employee = await self.employee_service.find_employee(email=username)
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
