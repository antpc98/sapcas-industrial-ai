from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Material(Base):
    __tablename__ = "materials"

    id: Mapped[str] = mapped_column("material_id", String(32), primary_key=True)
    code: Mapped[str] = mapped_column("material_code", String(100), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    material_group: Mapped[str] = mapped_column(String(100), nullable=False)
    material_type: Mapped[str] = mapped_column(String(50), nullable=False)
    base_unit: Mapped[str] = mapped_column(String(20), nullable=False)
    criticality: Mapped[str] = mapped_column(String(20), nullable=False)
    certification_required: Mapped[str | None] = mapped_column(String(100), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
