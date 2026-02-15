from fastapi import APIRouter
from backend.app.schemas.prediction import PricingRequest, PricingResponse
from backend.app.services.feature_service import FeatureEngineeringService
from backend.app.services.ml_service import PricingModelService
from backend.app.services.price_adjustment_service import PriceAdjustmentService

router = APIRouter(prefix="/api", tags=["Pricing"])

feature = FeatureEngineeringService()
ml = PricingModelService()
adjust = PriceAdjustmentService()

@router.post("/predict", response_model=PricingResponse)
def predict(req: PricingRequest):
    features = feature.transform(req)
    ml_price = ml.predict(features)

    final = adjust.adjust(
        ml_price=ml_price,
        category=req.product_type,
        brand=req.brand,
        weight=req.weight,
        market_price=req.market_price if hasattr(req,"market_price") else None,
        cost_price=None
    )

    return PricingResponse(
        predicted_price=final,
        ml_price=ml_price,
        market_price=None,
        cost_price=None,
        confidence="High"
    )