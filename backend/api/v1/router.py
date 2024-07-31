from fastapi import APIRouter

from api.v1.routers import auth_router
from api.v1.routers import employees_router
from api.v1.routers import health_profiles_router
from api.v1.routers import medical_records_router
from api.v1.routers import patients_router
from api.v1.routers import prescriptions_router

router = APIRouter(prefix="/v1")
router.include_router(auth_router)
router.include_router(employees_router)
router.include_router(patients_router)
router.include_router(health_profiles_router)
router.include_router(medical_records_router)
router.include_router(prescriptions_router)
