from fastapi import APIRouter, Depends

from bloca_ml.core.security import api_key_auth

router = APIRouter(
    prefix="/predict", tags=["predict"], dependencies=[Depends(api_key_auth)]
)


@router.post("/strength/")
def predict_strength():
    return {"message": "Strength prediction endpoint"}


@router.post("/surface/")
def predict_surface():
    return {"message": "Surface prediction endpoint"}
