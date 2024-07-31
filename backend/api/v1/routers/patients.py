from fastapi import APIRouter, Depends, Query

from api.deps import UOWDep, require_roles
from dtos.pagination import PaginationResponse
from dtos.patient import PatientResponse, PatientCreateRequest, PatientUpdate, PatientCreateResponse
from enums.employee import admin_doctor_nurse
from services import patient_service

router = APIRouter(prefix="/patients", tags=["Patients"], dependencies=[Depends(require_roles(*admin_doctor_nurse))])


@router.post("/", response_model=PatientCreateResponse, status_code=201)
async def create_patient(data: PatientCreateRequest, uow: UOWDep):
    patient = await patient_service.create(uow, data=data)
    return patient


@router.get("/", response_model=PaginationResponse[PatientResponse])
async def find_all_patients(
        uow: UOWDep,
        limit: int = Query(default=10, ge=0),
        offset: int = Query(default=0, ge=0)
):
    patients = await patient_service.find_all(uow, limit=limit, offset=offset)
    return patients


@router.get("/{patient_id}/", response_model=PatientResponse)
async def find_patient_by_id(patient_id: int, uow: UOWDep):
    patient = await patient_service.find_patient(uow, id=patient_id)
    return patient


@router.patch("/{patient_id}/", response_model=PatientResponse)
async def update_patient(patient_id: int, data: PatientUpdate, uow: UOWDep):
    patient = await patient_service.update(uow, patient_id=patient_id, data=data)
    return patient
