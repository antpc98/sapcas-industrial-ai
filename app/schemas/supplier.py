from pydantic import BaseModel, ConfigDict


class SupplierRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    code: str
    name: str
    country: str
    currency: str
    payment_terms_days: int
    reliability_score: float
    quality_score: float
    active: bool
