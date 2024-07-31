from fastapi import APIRouter, Depends

from api.deps import UOWDep, require_roles
from dtos.prescription import PrescriptionCreateRequest, PrescriptionCreateResponse, PrescriptionResponse
from enums.employee import admin_doctor_nurse
from services import prescription_service

router = APIRouter(prefix="/prescriptions", tags=["Prescriptions"], dependencies=[Depends(require_roles(*admin_doctor_nurse))])


@router.post("/", response_model=PrescriptionCreateResponse, status_code=201)
async def create_prescription(uow: UOWDep, data: PrescriptionCreateRequest):
    prescription = await prescription_service.create(uow, data=data)
    return prescription


@router.get("/{medical_record_id}/", response_model=PrescriptionResponse)
async def find_prescription_by_medical_record_id(uow: UOWDep, medical_record_id: int):
    medical_record = await prescription_service.find_prescription(uow, medical_record_id=medical_record_id)
    return medical_record


@router.delete("/{medical_record_id}/", status_code=204)
async def delete_prescription_by_medical_record_id(uow: UOWDep, medical_record_id: int):
    await prescription_service.delete_prescription(uow, medical_record_id=medical_record_id)
