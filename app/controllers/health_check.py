from fastapi import APIRouter, Depends

from app.services.health_service import HealthService

router = APIRouter(prefix="/health")


@router.get(
    "/", description="Verificação da saúde da API e serviços associados", response_model=bool
)
async def health_check(healthService: HealthService = Depends()):
    return await healthService.check_health()
