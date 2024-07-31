from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.unitofwork import UnitOfWork
    from dtos.auth import Token, AccessToken
    from models import Employee


class AuthService(ABC):
    @abstractmethod
    async def login(self, uow: "UnitOfWork", *, username: str, password: str) -> "Token":
        pass

    @abstractmethod
    async def refresh_token(self, token: str) -> "AccessToken":
        pass

    @abstractmethod
    async def authenticate(self, uow: "UnitOfWork", *, username: str, password: str) -> "Employee":
        pass
