from typing import TYPE_CHECKING

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from services.prescription.service import PrescriptionService

if TYPE_CHECKING:
    from core.unitofwork import UnitOfWork
    from dtos.prescription import PrescriptionCreateRequest
    from models import Prescription


class PrescriptionServiceImpl(PrescriptionService):
    async def create(self, uow: "UnitOfWork", *, data: "PrescriptionCreateRequest") -> "Prescription":
        try:
            async with uow:
                prescription = await uow.prescription.create(**data.model_dump())
                return prescription
        except IntegrityError:
            raise HTTPException(
                status_code=404,
                detail="Medical record not found"
            )

    async def find_prescription(self, uow: "UnitOfWork", **kwargs) -> "Prescription":
        async with uow:
            prescription = await uow.prescription.filter(**kwargs)
            if not prescription:
                raise HTTPException(
                    status_code=404,
                    detail="Prescription not found"
                )
            return prescription

    async def delete_prescription(self, uow: "UnitOfWork", **kwargs) -> None:
        async with uow:
            prescription = await uow.prescription.filter(**kwargs)
            if not prescription:
                raise HTTPException(
                    status_code=404,
                    detail="Prescription not found"
                )
            await uow.prescription.delete(prescription)


prescription_service = PrescriptionServiceImpl()
