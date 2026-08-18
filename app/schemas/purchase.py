from datetime import date

from pydantic import BaseModel, ConfigDict


class PurchaseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    purchase_order_id: str
    purchase_order_line: int
    company_id: str
    plant_id: str
    supplier_id: str
    material_id: str
    order_date: date
    expected_delivery_date: date
    actual_delivery_date: date | None
    quantity: float
    unit_price: float
    currency: str
    transport_cost: float
    status: str
