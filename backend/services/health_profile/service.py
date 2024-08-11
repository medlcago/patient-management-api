from typing import TYPE_CHECKING, Sequence

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from services.health_profile.interface import HealthProfileServiceInterface

if TYPE_CHECKING:
    from dtos.health_profile import HealthProfileCreateRequest
    from core.unitofwork import UnitOfWork
    from models import HealthProfile


class HealthProfileService(HealthProfileServiceInterface):
    def __init__(self, uow: "UnitOfWork"):
        self.uow = uow

    async def create(self, *, data: "HealthProfileCreateRequest") -> "HealthProfile":
        try:
            async with self.uow:
                if await self.uow.health_profile.filter(patient_id=data.patient_id):
                    raise HTTPException(
                        status_code=409,
                        detail="Health profile already exists",
                    )
                health_profile = await self.uow.health_profile.create(**data.model_dump())
                return health_profile
        except IntegrityError:
            raise HTTPException(
                status_code=404,
                detail="Patient not found"
            )

    async def find_all(
            self,
            *options,
            limit: int,
            offset: int,
            order_by: tuple[str, bool] | None = None,
            **kwargs
    ) -> dict[str, int | Sequence["HealthProfile"]]:
        async with self.uow:
            health_profiles = await self.uow.health_profile.find_all(
                limit=limit,
                offset=offset,
                order_by=order_by,
                *options,
                **kwargs
            )
            return health_profiles

    async def find_health_profile(self, **kwargs) -> "HealthProfile":
        async with self.uow:
            health_profile = await self.uow.health_profile.filter(**kwargs)
            if not health_profile:
                raise HTTPException(
                    status_code=404,
                    detail="Health profile not found"
                )
            return health_profile
