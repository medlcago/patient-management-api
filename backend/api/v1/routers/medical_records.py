from fastapi import APIRouter, Query, Depends

from api.deps import UOWDep, require_roles, currentActiveEmployeeDep
from dtos.medical_record import MedicalRecordCreateResponse, MedicalRecordCreateRequest, MedicalRecordResponse
from dtos.pagination import PaginationResponse
from enums.employee import admin_doctor_nurse
from services import medical_record_service

router = APIRouter(prefix="/medical-records", tags=["Medical Records"], dependencies=[Depends(require_roles(*admin_doctor_nurse))])


@router.post("/", response_model=MedicalRecordCreateResponse, status_code=201)
async def create_medical_record(
        uow: UOWDep,
        employee: currentActiveEmployeeDep,
        data: MedicalRecordCreateRequest
):
    medical_record = await medical_record_service.create(uow, employee_id=employee.id, data=data)
    return medical_record


@router.get("/", response_model=PaginationResponse[MedicalRecordResponse])
async def find_all_medical_records(
        uow: UOWDep,
        limit: int = Query(default=10, ge=0),
        offset: int = Query(default=0, ge=0)
):
    return await medical_record_service.find_all(uow, limit=limit, offset=offset)


@router.get("/{patient_id}/", response_model=PaginationResponse[MedicalRecordResponse])
async def find_medical_records_by_patient_id(
        uow: UOWDep,
        patient_id: int,
        limit: int = Query(default=10, ge=0),
        offset: int = Query(default=0, ge=0)
):
    return await medical_record_service.find_all(uow, limit=limit, offset=offset, patient_id=patient_id)
