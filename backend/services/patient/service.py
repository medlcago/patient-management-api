from typing import TYPE_CHECKING, Sequence

from fastapi import HTTPException

from services.patient.interface import PatientServiceInterface

if TYPE_CHECKING:
    from dtos.patient import PatientCreateRequest
    from dtos.patient import PatientUpdate
    from core.unitofwork import UnitOfWork
    from models import Patient


class PatientService(PatientServiceInterface):
    def __init__(self, uow: "UnitOfWork"):
        self.uow = uow

    async def create(self, *, data: "PatientCreateRequest") -> "Patient":
        async with self.uow:
            patient = await self.uow.patient.create(**data.model_dump())
            return patient

    async def find_all(
            self,
            *options,
            limit: int,
            offset: int,
            order_by: tuple[str, bool] | None = None,
            **kwargs
    ) -> dict[str, int | Sequence["Patient"]]:
        async with self.uow:
            patients = await self.uow.patient.find_all(
                limit=limit,
                offset=offset,
                order_by=order_by,
                *options,
                **kwargs
            )
            return patients

    async def find_patient(self, **kwargs) -> "Patient":
        async with self.uow:
            patient = await self.uow.patient.filter(**kwargs)
            if not patient:
                raise HTTPException(
                    status_code=404,
                    detail=f"Patient not found"
                )
            return patient

    async def update(self, *, patient_id: int, data: "PatientUpdate") -> "Patient":
        async with self.uow:
            patient = await self.uow.patient.update(patient_id, **data.model_dump(exclude_none=True))
            if not patient:
                raise HTTPException(
                    status_code=404,
                    detail=f"Patient not found"
                )
            return patient
