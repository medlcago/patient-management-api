from typing import TYPE_CHECKING, Sequence

from fastapi import HTTPException

from services.patient.service import PatientService

if TYPE_CHECKING:
    from dtos.patient import PatientCreateRequest
    from dtos.patient import PatientUpdate
    from core.unitofwork import UnitOfWork
    from models import Patient


class PatientServiceImpl(PatientService):
    async def create(self, uow: "UnitOfWork", *, data: "PatientCreateRequest") -> "Patient":
        async with uow:
            patient = await uow.patient.create(**data.model_dump())
            return patient

    async def find_all(
            self, uow: "UnitOfWork",
            *options,
            limit: int,
            offset: int,
            order_by: tuple[str, bool] | None = None,
            **kwargs
    ) -> dict[str, int | Sequence["Patient"]]:
        async with uow:
            patients = await uow.patient.find_all(limit=limit, offset=offset, order_by=order_by, *options, **kwargs)
            return patients

    async def find_patient(self, uow: "UnitOfWork", **kwargs) -> "Patient":
        async with uow:
            patient = await uow.patient.filter(**kwargs)
            if not patient:
                raise HTTPException(
                    status_code=404,
                    detail=f"Patient not found"
                )
            return patient

    async def update(self, uow: "UnitOfWork", *, patient_id: int, data: "PatientUpdate") -> "Patient":
        async with uow:
            patient = await uow.patient.update(patient_id, **data.model_dump(exclude_none=True))
            if not patient:
                raise HTTPException(
                    status_code=404,
                    detail=f"Patient not found"
                )
            return patient


patient_service = PatientServiceImpl()
