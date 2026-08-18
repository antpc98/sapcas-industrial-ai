from datetime import date

from sqlalchemy import Date, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Purchase(Base):
    __tablename__ = "purchases"
    __table_args__ = (
        UniqueConstraint("purchase_order_id", "purchase_order_line", name="uq_purchase_order_line"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    purchase_order_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    purchase_order_line: Mapped[int] = mapped_column(Integer, nullable=False)

    company_id: Mapped[str] = mapped_column(ForeignKey("companies.company_id"), nullable=False, index=True)
    plant_id: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    supplier_id: Mapped[str] = mapped_column(ForeignKey("suppliers.supplier_id"), nullable=False, index=True)
    material_id: Mapped[str] = mapped_column(ForeignKey("materials.material_id"), nullable=False, index=True)

    order_date: Mapped[date] = mapped_column(Date, nullable=False)
    expected_delivery_date: Mapped[date] = mapped_column(Date, nullable=False)
    actual_delivery_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    transport_cost: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
