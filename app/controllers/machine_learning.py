from fastapi import APIRouter, Body, Depends, HTTPException

from app.dtos.ml import BookFeatureDto, PredictionInputDto, PredictionOutputDto, TrainingDataDto
from app.services.ml_service import MachineLearningService

router = APIRouter(prefix="/ml")


@router.get(
    "/features",
    description="Extrai features dos livros para análise de machine learning",
    response_model=list[BookFeatureDto],
)
async def get_features(mlService: MachineLearningService = Depends()):
    return await mlService.extract_features()


@router.get(
    "/training-data",
    description="Gera e retorna os dados de treinamento que serão usados por um modelo de Machine Learning.",
    response_model=TrainingDataDto,
)
async def get_training_data(mlService: MachineLearningService = Depends()):
    x, y = await mlService.get_training_data()
    return {"features": x.tolist(), "labels": y.tolist()}


@router.post(
    "/training",
    description="Treina e salva um modelo de Machine Learning",
)
async def post_training(mlService: MachineLearningService = Depends()):
    return await mlService.train_model()


@router.post(
    "/predictions",
    description="Realiza a predição de preços com base no rating fornecido.",
    response_model=PredictionOutputDto,
)
async def post_predictions(
    mlService: MachineLearningService = Depends(), payload: PredictionInputDto = Body(...)
):
    try:
        return mlService.predict(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
