from fastapi import APIRouter, Depends

from api.deps import require_roles, ServiceDep
from dtos.prescription import PrescriptionCreateRequest, PrescriptionCreateResponse, PrescriptionResponse
from enums.employee import admin_doctor_nurse

router = APIRouter(prefix="/prescriptions", tags=["Prescriptions"], dependencies=[Depends(require_roles(*admin_doctor_nurse))])


@router.post("/", response_model=PrescriptionCreateResponse, status_code=201)
async def create_prescription(service: ServiceDep, data: PrescriptionCreateRequest):
    prescription = await service.prescription_service.create(data=data)
    return prescription


@router.get("/{medical_record_id}/", response_model=PrescriptionResponse)
async def find_prescription_by_medical_record_id(service: ServiceDep, medical_record_id: int):
    medical_record = await service.prescription_service.find_prescription(medical_record_id=medical_record_id)
    return medical_record


@router.delete("/{medical_record_id}/", status_code=204)
async def delete_prescription_by_medical_record_id(service: ServiceDep, medical_record_id: int):
    await service.prescription_service.delete_prescription(medical_record_id=medical_record_id)
