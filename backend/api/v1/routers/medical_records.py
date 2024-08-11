from fastapi import APIRouter, Query, Depends

from api.deps import require_roles, currentActiveEmployeeDep, ServiceDep
from dtos.medical_record import MedicalRecordCreateResponse, MedicalRecordCreateRequest, MedicalRecordResponse
from dtos.pagination import PaginationResponse
from enums.employee import admin_doctor_nurse

router = APIRouter(prefix="/medical-records", tags=["Medical Records"], dependencies=[Depends(require_roles(*admin_doctor_nurse))])


@router.post("/", response_model=MedicalRecordCreateResponse, status_code=201)
async def create_medical_record(
        service: ServiceDep,
        employee: currentActiveEmployeeDep,
        data: MedicalRecordCreateRequest
):
    medical_record = await service.medical_record_service.create(employee_id=employee.id, data=data)
    return medical_record


@router.get("/", response_model=PaginationResponse[MedicalRecordResponse])
async def find_all_medical_records(
        service: ServiceDep,
        limit: int = Query(default=10, ge=0),
        offset: int = Query(default=0, ge=0)
):
    return await service.medical_record_service.find_all(limit=limit, offset=offset)


@router.get("/{patient_id}/", response_model=PaginationResponse[MedicalRecordResponse])
async def find_medical_records_by_patient_id(
        service: ServiceDep,
        patient_id: int,
        limit: int = Query(default=10, ge=0),
        offset: int = Query(default=0, ge=0)
):
    return await service.medical_record_service.find_all(limit=limit, offset=offset, patient_id=patient_id)
