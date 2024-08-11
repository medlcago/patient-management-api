from fastapi import APIRouter, Depends, Query

from api.deps import require_roles, ServiceDep
from dtos.health_profile import HealthProfileCreateRequest, HealthProfileCreateResponse, HealthProfileResponse
from dtos.pagination import PaginationResponse
from enums.employee import admin_doctor_nurse

router = APIRouter(prefix="/health-profiles", tags=["Health Profiles"], dependencies=[Depends(require_roles(*admin_doctor_nurse))])


@router.post("/", response_model=HealthProfileCreateResponse, status_code=201)
async def create_health_profile(data: HealthProfileCreateRequest, service: ServiceDep):
    health_profile = await service.health_profile_service.create(data=data)
    return health_profile


@router.get("/", response_model=PaginationResponse[HealthProfileResponse])
async def find_all_health_profiles(
        service: ServiceDep,
        limit: int = Query(default=10, ge=0),
        offset: int = Query(default=0, ge=0)
):
    health_profiles = await service.health_profile_service.find_all(limit=limit, offset=offset)
    return health_profiles


@router.get("/{patient_id}/", response_model=HealthProfileResponse)
async def find_health_profile_by_patient_id(patient_id: int, service: ServiceDep):
    health_profile = await service.health_profile_service.find_health_profile(patient_id=patient_id)
    return health_profile
