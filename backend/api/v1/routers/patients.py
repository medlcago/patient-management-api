from fastapi import APIRouter, Depends, Query

from api.deps import require_roles, ServiceDep
from dtos.pagination import PaginationResponse
from dtos.patient import PatientResponse, PatientCreateRequest, PatientUpdate, PatientCreateResponse
from enums.employee import admin_doctor_nurse

router = APIRouter(prefix="/patients", tags=["Patients"], dependencies=[Depends(require_roles(*admin_doctor_nurse))])


@router.post("/", response_model=PatientCreateResponse, status_code=201)
async def create_patient(data: PatientCreateRequest, service: ServiceDep):
    patient = await service.patient_service.create(data=data)
    return patient


@router.get("/", response_model=PaginationResponse[PatientResponse])
async def find_all_patients(
        service: ServiceDep,
        limit: int = Query(default=10, ge=0),
        offset: int = Query(default=0, ge=0)
):
    patients = await service.patient_service.find_all(limit=limit, offset=offset)
    return patients


@router.get("/{patient_id}/", response_model=PatientResponse)
async def find_patient_by_id(patient_id: int, service: ServiceDep):
    patient = await service.patient_service.find_patient(id=patient_id)
    return patient


@router.patch("/{patient_id}/", response_model=PatientResponse)
async def update_patient(patient_id: int, data: PatientUpdate, service: ServiceDep):
    patient = await service.patient_service.update(patient_id=patient_id, data=data)
    return patient
