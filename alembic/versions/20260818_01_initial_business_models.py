"""initial business models

Revision ID: 20260818_01
Revises:
Create Date: 2026-08-18
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260818_01"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "companies",
        sa.Column("company_id", sa.String(length=32), primary_key=True),
        sa.Column("company_name", sa.String(length=255), nullable=False),
        sa.Column("country", sa.String(length=2), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("industry", sa.String(length=255), nullable=False),
        sa.Column("notes", sa.String(length=500), nullable=True),
    )

    op.create_table(
        "materials",
        sa.Column("material_id", sa.String(length=32), primary_key=True),
        sa.Column("material_code", sa.String(length=100), nullable=False, unique=True),
        sa.Column("description", sa.String(length=255), nullable=False),
        sa.Column("material_group", sa.String(length=100), nullable=False),
        sa.Column("material_type", sa.String(length=50), nullable=False),
        sa.Column("base_unit", sa.String(length=20), nullable=False),
        sa.Column("criticality", sa.String(length=20), nullable=False),
        sa.Column("certification_required", sa.String(length=100), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False),
    )
    op.create_index("ix_materials_material_code", "materials", ["material_code"], unique=False)

    op.create_table(
        "suppliers",
        sa.Column("supplier_id", sa.String(length=32), primary_key=True),
        sa.Column("supplier_code", sa.String(length=50), nullable=False, unique=True),
        sa.Column("supplier_name", sa.String(length=255), nullable=False),
        sa.Column("country", sa.String(length=2), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("payment_terms_days", sa.Integer(), nullable=False),
        sa.Column("reliability_score", sa.Float(), nullable=False),
        sa.Column("quality_score", sa.Float(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
    )
    op.create_index("ix_suppliers_supplier_code", "suppliers", ["supplier_code"], unique=False)

    op.create_table(
        "inventory_items",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("plant_id", sa.String(length=32), nullable=False),
        sa.Column("warehouse_id", sa.String(length=32), nullable=False),
        sa.Column("material_id", sa.String(length=32), sa.ForeignKey("materials.material_id"), nullable=False),
        sa.Column("on_hand_quantity", sa.Float(), nullable=False),
        sa.Column("reserved_quantity", sa.Float(), nullable=False),
        sa.Column("available_quantity", sa.Float(), nullable=False),
        sa.Column("safety_stock", sa.Float(), nullable=False),
        sa.Column("average_daily_consumption", sa.Float(), nullable=False),
        sa.Column("average_unit_cost", sa.Float(), nullable=False),
        sa.Column("last_movement_date", sa.Date(), nullable=False),
        sa.UniqueConstraint("plant_id", "warehouse_id", "material_id", name="uq_inventory_location_material"),
    )
    op.create_index("ix_inventory_items_plant_id", "inventory_items", ["plant_id"], unique=False)
    op.create_index("ix_inventory_items_warehouse_id", "inventory_items", ["warehouse_id"], unique=False)
    op.create_index("ix_inventory_items_material_id", "inventory_items", ["material_id"], unique=False)

    op.create_table(
        "purchases",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("purchase_order_id", sa.String(length=50), nullable=False),
        sa.Column("purchase_order_line", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.String(length=32), sa.ForeignKey("companies.company_id"), nullable=False),
        sa.Column("plant_id", sa.String(length=32), nullable=False),
        sa.Column("supplier_id", sa.String(length=32), sa.ForeignKey("suppliers.supplier_id"), nullable=False),
        sa.Column("material_id", sa.String(length=32), sa.ForeignKey("materials.material_id"), nullable=False),
        sa.Column("order_date", sa.Date(), nullable=False),
        sa.Column("expected_delivery_date", sa.Date(), nullable=False),
        sa.Column("actual_delivery_date", sa.Date(), nullable=True),
        sa.Column("quantity", sa.Float(), nullable=False),
        sa.Column("unit_price", sa.Float(), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("transport_cost", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.UniqueConstraint("purchase_order_id", "purchase_order_line", name="uq_purchase_order_line"),
    )
    op.create_index("ix_purchases_purchase_order_id", "purchases", ["purchase_order_id"], unique=False)
    op.create_index("ix_purchases_company_id", "purchases", ["company_id"], unique=False)
    op.create_index("ix_purchases_plant_id", "purchases", ["plant_id"], unique=False)
    op.create_index("ix_purchases_supplier_id", "purchases", ["supplier_id"], unique=False)
    op.create_index("ix_purchases_material_id", "purchases", ["material_id"], unique=False)


def downgrade() -> None:
    op.drop_table("purchases")
    op.drop_table("inventory_items")
    op.drop_table("suppliers")
    op.drop_table("materials")
    op.drop_table("companies")
