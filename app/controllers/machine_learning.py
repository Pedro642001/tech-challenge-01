from fastapi import APIRouter, Body, Depends, HTTPException

from app.services.ml_service import MachineLearningService

router = APIRouter(prefix="/ml")


@router.get("/features", description="Extrai features de um texto")
async def get_features(mlService: MachineLearningService = Depends()):
    return await mlService.extract_features()


@router.get(
    "/training-data",
    description="Extrai dados de treinamento",
)
async def get_training_data(mlService: MachineLearningService = Depends()):
    x, y = await mlService.get_training_data()
    return {"features": x.tolist(), "labels": y.tolist()}


@router.post("/training", description="Treina um modelo")
async def post_training(mlService: MachineLearningService = Depends()):
    return await mlService.train_model()


@router.post("/predictions", description="Recebe predições de um modelo")
async def post_predictions(
    mlService: MachineLearningService = Depends(), payload: dict = Body(...)
):
    try:
        return mlService.predict(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
