from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dtos.auth import Token, AccessToken
    from models import Employee


class AuthServiceInterface(ABC):
    @abstractmethod
    async def login(self, *, username: str, password: str) -> "Token":
        pass

    @abstractmethod
    async def refresh_token(self, *, token: str) -> "AccessToken":
        pass

    @abstractmethod
    async def authenticate(self, *, username: str, password: str) -> "Employee":
        pass
