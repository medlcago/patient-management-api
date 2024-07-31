from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.deps import UOWDep
from dtos.auth import Token, AccessToken, RefreshToken
from services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token/", response_model=Token, response_model_exclude_none=True)
async def access_token(uow: UOWDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    token = await auth_service.login(uow, username=form_data.username, password=form_data.password)
    return token


@router.post("/token/refresh/", response_model=AccessToken)
async def refresh_token(refresh: RefreshToken):
    access = await auth_service.refresh_token(token=refresh.refresh_token)
    return access
