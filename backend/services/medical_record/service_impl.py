from typing import TYPE_CHECKING, Sequence

from fastapi import HTTPException

from services.medical_record.service import MedicalRecordService

if TYPE_CHECKING:
    from core.unitofwork import UnitOfWork
    from dtos.medical_record import MedicalRecordCreateRequest
    from models import MedicalRecord


class MedicalRecordServiceImpl(MedicalRecordService):
    async def create(
            self,
            uow: "UnitOfWork",
            *,
            employee_id: int,
            data: "MedicalRecordCreateRequest"
    ) -> "MedicalRecord":
        async with uow:
            if not await uow.patient.filter(id=data.patient_id):
                raise HTTPException(
                    status_code=404,
                    detail="Patient not found"
                )
            medical_record = await uow.medical_record.create(employee_id=employee_id, **data.model_dump())
            return medical_record

    async def find_all(
            self,
            uow: "UnitOfWork",
            *options,
            limit: int,
            offset: int,
            order_by: tuple[str, bool] | None = None,
            **kwargs
    ) -> dict[str, int | Sequence["MedicalRecord"]]:
        async with uow:
            medical_records = await uow.medical_record.find_all(
                limit=limit,
                offset=offset,
                order_by=order_by,
                *options,
                **kwargs
            )
            return medical_records

    async def find_medical_record(self, uow: "UnitOfWork", **kwargs) -> "MedicalRecord":
        async with uow:
            medical_record = await uow.medical_record.filter(**kwargs)
            if not medical_record:
                raise HTTPException(
                    status_code=404,
                    detail="Medical record not found"
                )
            return medical_record


medical_record_service = MedicalRecordServiceImpl()
