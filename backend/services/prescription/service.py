from typing import TYPE_CHECKING

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from services.prescription.interface import PrescriptionServiceInterface

if TYPE_CHECKING:
    from core.unitofwork import UnitOfWork
    from dtos.prescription import PrescriptionCreateRequest
    from models import Prescription


class PrescriptionService(PrescriptionServiceInterface):
    def __init__(self, uow: "UnitOfWork"):
        self.uow = uow

    async def create(self, *, data: "PrescriptionCreateRequest") -> "Prescription":
        try:
            async with self.uow:
                prescription = await self.uow.prescription.create(**data.model_dump())
                return prescription
        except IntegrityError:
            raise HTTPException(
                status_code=404,
                detail="Medical record not found"
            )

    async def find_prescription(self, **kwargs) -> "Prescription":
        async with self.uow:
            prescription = await self.uow.prescription.filter(**kwargs)
            if not prescription:
                raise HTTPException(
                    status_code=404,
                    detail="Prescription not found"
                )
            return prescription

    async def delete_prescription(self, **kwargs) -> None:
        async with self.uow:
            prescription = await self.uow.prescription.filter(**kwargs)
            if not prescription:
                raise HTTPException(
                    status_code=404,
                    detail="Prescription not found"
                )
            await self.uow.prescription.delete(prescription)
