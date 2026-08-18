from datetime import date

from sqlalchemy import Date, Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class InventoryItem(Base):
    __tablename__ = "inventory_items"
    __table_args__ = (
        UniqueConstraint("plant_id", "warehouse_id", "material_id", name="uq_inventory_location_material"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    plant_id: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    warehouse_id: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    material_id: Mapped[str] = mapped_column(ForeignKey("materials.material_id"), nullable=False, index=True)

    on_hand_quantity: Mapped[float] = mapped_column(Float, nullable=False)
    reserved_quantity: Mapped[float] = mapped_column(Float, nullable=False)
    available_quantity: Mapped[float] = mapped_column(Float, nullable=False)
    safety_stock: Mapped[float] = mapped_column(Float, nullable=False)
    average_daily_consumption: Mapped[float] = mapped_column(Float, nullable=False)
    average_unit_cost: Mapped[float] = mapped_column(Float, nullable=False)
    last_movement_date: Mapped[date] = mapped_column(Date, nullable=False)
