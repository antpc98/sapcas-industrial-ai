from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models import InventoryItem, Material, Purchase, Supplier
from app.schemas import InventoryItemRead, MaterialRead, PurchaseRead, SupplierRead

router = APIRouter(prefix="/api/v1")


@router.get("/", tags=["system"])
def api_root() -> dict[str, str]:
    return {
        "service": "SAPCAS Industrial AI",
        "version": "0.1.0",
    }


@router.get("/materials", response_model=list[MaterialRead], tags=["materials"])
def list_materials(db: Session = Depends(get_db)) -> list[Material]:
    return list(db.scalars(select(Material).order_by(Material.code)).all())


@router.get("/suppliers", response_model=list[SupplierRead], tags=["suppliers"])
def list_suppliers(db: Session = Depends(get_db)) -> list[Supplier]:
    return list(db.scalars(select(Supplier).order_by(Supplier.name)).all())


@router.get("/inventory", response_model=list[InventoryItemRead], tags=["inventory"])
def list_inventory(db: Session = Depends(get_db)) -> list[InventoryItem]:
    return list(db.scalars(select(InventoryItem).order_by(InventoryItem.material_id)).all())


@router.get("/purchases", response_model=list[PurchaseRead], tags=["purchases"])
def list_purchases(db: Session = Depends(get_db)) -> list[Purchase]:
    return list(
        db.scalars(
            select(Purchase).order_by(Purchase.order_date.desc(), Purchase.purchase_order_id)
        ).all()
    )
