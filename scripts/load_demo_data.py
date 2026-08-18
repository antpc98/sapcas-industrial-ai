from pathlib import Path

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models import Company, InventoryItem, Material, Purchase, Supplier

DATASET_ROOT = Path(__file__).resolve().parents[1] / "datasets" / "demo"


def _bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def validate_required_columns(df: pd.DataFrame, required: set[str], dataset_name: str) -> None:
    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            f"{dataset_name}: faltan columnas obligatorias: {sorted(missing)}"
        )


def upsert_company(db: Session, row: pd.Series) -> None:
    obj = db.get(Company, str(row.company_id))
    values = {
        "name": str(row.company_name),
        "country": str(row.country),
        "currency": str(row.currency),
        "industry": str(row.industry),
        "notes": None if pd.isna(row.notes) else str(row.notes),
    }
    if obj is None:
        db.add(Company(id=str(row.company_id), **values))
    else:
        for key, value in values.items():
            setattr(obj, key, value)


def upsert_material(db: Session, row: pd.Series) -> None:
    obj = db.get(Material, str(row.material_id))
    values = {
        "code": str(row.material_code),
        "description": str(row.description),
        "material_group": str(row.material_group),
        "material_type": str(row.material_type),
        "base_unit": str(row.base_unit),
        "criticality": str(row.criticality),
        "certification_required": None
        if pd.isna(row.certification_required)
        else str(row.certification_required),
        "active": _bool(row.active),
    }
    if obj is None:
        db.add(Material(id=str(row.material_id), **values))
    else:
        for key, value in values.items():
            setattr(obj, key, value)


def upsert_supplier(db: Session, row: pd.Series) -> None:
    obj = db.get(Supplier, str(row.supplier_id))
    values = {
        "code": str(row.supplier_code),
        "name": str(row.supplier_name),
        "country": str(row.country),
        "currency": str(row.currency),
        "payment_terms_days": int(row.payment_terms_days),
        "reliability_score": float(row.reliability_score),
        "quality_score": float(row.quality_score),
        "active": _bool(row.active),
    }
    if obj is None:
        db.add(Supplier(id=str(row.supplier_id), **values))
    else:
        for key, value in values.items():
            setattr(obj, key, value)


def upsert_inventory(db: Session, row: pd.Series) -> None:
    stmt = select(InventoryItem).where(
        InventoryItem.plant_id == str(row.plant_id),
        InventoryItem.warehouse_id == str(row.warehouse_id),
        InventoryItem.material_id == str(row.material_id),
    )
    obj = db.scalar(stmt)

    values = {
        "on_hand_quantity": float(row.on_hand_quantity),
        "reserved_quantity": float(row.reserved_quantity),
        "available_quantity": float(row.available_quantity),
        "safety_stock": float(row.safety_stock),
        "average_daily_consumption": float(row.average_daily_consumption),
        "average_unit_cost": float(row.average_unit_cost),
        "last_movement_date": pd.to_datetime(row.last_movement_date).date(),
    }

    if obj is None:
        db.add(
            InventoryItem(
                plant_id=str(row.plant_id),
                warehouse_id=str(row.warehouse_id),
                material_id=str(row.material_id),
                **values,
            )
        )
    else:
        for key, value in values.items():
            setattr(obj, key, value)


def upsert_purchase(db: Session, row: pd.Series) -> None:
    stmt = select(Purchase).where(
        Purchase.purchase_order_id == str(row.purchase_order_id),
        Purchase.purchase_order_line == int(row.purchase_order_line),
    )
    obj = db.scalar(stmt)

    actual_delivery = (
        None
        if pd.isna(row.actual_delivery_date) or str(row.actual_delivery_date).strip() == ""
        else pd.to_datetime(row.actual_delivery_date).date()
    )

    values = {
        "company_id": str(row.company_id),
        "plant_id": str(row.plant_id),
        "supplier_id": str(row.supplier_id),
        "material_id": str(row.material_id),
        "order_date": pd.to_datetime(row.order_date).date(),
        "expected_delivery_date": pd.to_datetime(row.expected_delivery_date).date(),
        "actual_delivery_date": actual_delivery,
        "quantity": float(row.quantity),
        "unit_price": float(row.unit_price),
        "currency": str(row.currency),
        "transport_cost": float(row.transport_cost),
        "status": str(row.status),
    }

    if obj is None:
        db.add(
            Purchase(
                purchase_order_id=str(row.purchase_order_id),
                purchase_order_line=int(row.purchase_order_line),
                **values,
            )
        )
    else:
        for key, value in values.items():
            setattr(obj, key, value)


def load_demo_data() -> None:
    companies = pd.read_csv(DATASET_ROOT / "master" / "companies.csv")
    materials = pd.read_csv(DATASET_ROOT / "master" / "materials.csv")
    suppliers = pd.read_csv(DATASET_ROOT / "master" / "suppliers.csv")
    inventory = pd.read_csv(DATASET_ROOT / "transactions" / "inventory.csv")
    purchases = pd.read_csv(DATASET_ROOT / "transactions" / "purchase_orders.csv")

    validate_required_columns(
        companies,
        {"company_id", "company_name", "country", "currency", "industry", "notes"},
        "companies.csv",
    )
    validate_required_columns(
        materials,
        {
            "material_id",
            "material_code",
            "description",
            "material_group",
            "material_type",
            "base_unit",
            "criticality",
            "certification_required",
            "active",
        },
        "materials.csv",
    )
    validate_required_columns(
        suppliers,
        {
            "supplier_id",
            "supplier_code",
            "supplier_name",
            "country",
            "currency",
            "payment_terms_days",
            "reliability_score",
            "quality_score",
            "active",
        },
        "suppliers.csv",
    )
    validate_required_columns(
        inventory,
        {
            "plant_id",
            "warehouse_id",
            "material_id",
            "on_hand_quantity",
            "reserved_quantity",
            "available_quantity",
            "safety_stock",
            "average_daily_consumption",
            "average_unit_cost",
            "last_movement_date",
        },
        "inventory.csv",
    )
    validate_required_columns(
        purchases,
        {
            "purchase_order_id",
            "purchase_order_line",
            "company_id",
            "plant_id",
            "supplier_id",
            "material_id",
            "order_date",
            "expected_delivery_date",
            "actual_delivery_date",
            "quantity",
            "unit_price",
            "currency",
            "transport_cost",
            "status",
        },
        "purchase_orders.csv",
    )

    with SessionLocal() as db:
        for _, row in companies.iterrows():
            upsert_company(db, row)
        db.flush()

        for _, row in materials.iterrows():
            upsert_material(db, row)
        for _, row in suppliers.iterrows():
            upsert_supplier(db, row)
        db.flush()

        for _, row in inventory.iterrows():
            upsert_inventory(db, row)
        for _, row in purchases.iterrows():
            upsert_purchase(db, row)

        db.commit()

        print("Demo data cargados correctamente.")
        print(f"  Companies : {len(companies)}")
        print(f"  Materials : {len(materials)}")
        print(f"  Suppliers : {len(suppliers)}")
        print(f"  Inventory : {len(inventory)}")
        print(f"  Purchases : {len(purchases)}")


if __name__ == "__main__":
    load_demo_data()
