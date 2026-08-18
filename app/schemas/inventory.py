from datetime import date

from pydantic import BaseModel, ConfigDict


class InventoryItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    plant_id: str
    warehouse_id: str
    material_id: str
    on_hand_quantity: float
    reserved_quantity: float
    available_quantity: float
    safety_stock: float
    average_daily_consumption: float
    average_unit_cost: float
    last_movement_date: date
