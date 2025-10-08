from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.dtos.access_token import AccessTokenDto
from app.dtos.refresh_token import RefreshTokenDto
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth")


@router.post("/login", description="Login do usuário", response_model=AccessTokenDto)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    authService: AuthService = Depends(),
):
    user = await authService.authenticate_user(form_data.username, form_data.password)

    return AccessTokenDto(
        access_token=authService.create_access_token(data={"sub": str(user.id)}),
        refresh_token=authService.create_refresh_token(data={"sub": str(user.id)}),
    )


@router.post("/refresh", description="Refresh do token de acesso")
async def refresh_token(
    refresh_token_body: RefreshTokenDto,
    authService: AuthService = Depends(),
):
    authService.validate_refresh_token(refresh_token_body.refresh_token)

    user_id = authService.validate_access_token(refresh_token_body.access_token)

    return AccessTokenDto(
        access_token=authService.create_access_token(data={"sub": str(user_id)}),
        refresh_token=authService.create_refresh_token(data={"sub": str(user_id)}),
    )
