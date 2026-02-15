from pydantic import BaseModel
from typing import Optional, List

class PricingRequest(BaseModel):
    product_name: str
    weight: float
    fat_content: str
    product_type: str
    outlet_type: str
    outlet_size: str
    location_type: str
    establishment_year: int
    visibility: float


    brand: Optional[str] = "generic"

   
    ingredients: Optional[List[dict]] = None
    packaging_cost: Optional[float] = None
    labour_cost: Optional[float] = None
    transport_cost: Optional[float] = None
    gst_percent: Optional[float] = None



class PricingResponse(BaseModel):
    predicted_price: float
    confidence: str

 
    ml_price: Optional[float] = None
    market_price: Optional[float] = None
    cost_price: Optional[float] = None