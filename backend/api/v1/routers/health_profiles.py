from fastapi import APIRouter, Depends, Query

from api.deps import UOWDep, require_roles
from dtos.health_profile import HealthProfileCreateRequest, HealthProfileCreateResponse, HealthProfileResponse
from dtos.pagination import PaginationResponse
from enums.employee import admin_doctor_nurse
from services import health_profile_service

router = APIRouter(prefix="/health-profiles", tags=["Health Profiles"], dependencies=[Depends(require_roles(*admin_doctor_nurse))])


@router.post("/", response_model=HealthProfileCreateResponse, status_code=201)
async def create_health_profile(data: HealthProfileCreateRequest, uow: UOWDep):
    health_profile = await health_profile_service.create(uow, data=data)
    return health_profile


@router.get("/", response_model=PaginationResponse[HealthProfileResponse])
async def find_all_health_profiles(
        uow: UOWDep,
        limit: int = Query(default=10, ge=0),
        offset: int = Query(default=0, ge=0)
):
    health_profiles = await health_profile_service.find_all(uow, limit=limit, offset=offset)
    return health_profiles


@router.get("/{patient_id}/", response_model=HealthProfileResponse)
async def find_health_profile_by_patient_id(patient_id: int, uow: UOWDep):
    health_profile = await health_profile_service.find_health_profile(uow, patient_id=patient_id)
    return health_profile
