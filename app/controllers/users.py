from fastapi import APIRouter, Depends

from app.dtos.create_user_dto import CreateUserDto
from app.models.user import get_user_dto
from app.services.user_service import UserService
from app.utils.filter import Filter

router = APIRouter(prefix="/users")


@router.post(
    "/register",
    description="Registrar um novo usuário",
    status_code=201,
    response_model=None,
)
async def create_user(user: CreateUserDto, userService: UserService = Depends()):
    userService.create(user)
    pass


@router.get("/", description="Listar todos os usuários", response_model=list[get_user_dto])
async def list_users(filter: Filter = Depends(), userService: UserService = Depends()):
    return await get_user_dto.from_queryset(userService.get_users(filter))
