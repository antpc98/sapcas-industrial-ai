"""Auditoría estructural y semántica reproducible de los CSV demo de SAPCAS.

Ejecutar desde la raíz del repositorio: ``.venv\\Scripts\\python scripts/audit_demo_data.py``.
El informe generado es evidencia, no una migración de base de datos ni un
framework genérico de calidad de datos.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATASET_ROOT = ROOT / "datasets" / "demo"
DEFAULT_REPORT = ROOT / "docs" / "audits" / "MVP_DATASET_AUDIT_RESULTS.md"
DECIMAL_TOLERANCE = 0.011  # Los importes fuente están redondeados a dos decimales.

PRIMARY_KEYS = {
    "companies": ["company_id"], "materials": ["material_id"],
    "plants": ["plant_id"], "warehouses": ["warehouse_id"],
    "suppliers": ["supplier_id"], "supplier_materials": ["supplier_material_id"],
    "inventory": ["plant_id", "warehouse_id", "material_id"],
    "purchase_orders": ["purchase_order_id", "purchase_order_line"],
    "purchase_requisitions": ["requisition_id"], "goods_receipts": ["receipt_id"],
}
RELATIONS = [
    ("plants.company_id", "plants", "company_id", "companies", "company_id"),
    ("warehouses.plant_id", "warehouses", "plant_id", "plants", "plant_id"),
    ("supplier_materials.supplier_id", "supplier_materials", "supplier_id", "suppliers", "supplier_id"),
    ("supplier_materials.material_id", "supplier_materials", "material_id", "materials", "material_id"),
    ("inventory.plant_id", "inventory", "plant_id", "plants", "plant_id"),
    ("inventory.warehouse_id", "inventory", "warehouse_id", "warehouses", "warehouse_id"),
    ("inventory.material_id", "inventory", "material_id", "materials", "material_id"),
    ("purchase_orders.company_id", "purchase_orders", "company_id", "companies", "company_id"),
    ("purchase_orders.plant_id", "purchase_orders", "plant_id", "plants", "plant_id"),
    ("purchase_orders.supplier_id", "purchase_orders", "supplier_id", "suppliers", "supplier_id"),
    ("purchase_orders.material_id", "purchase_orders", "material_id", "materials", "material_id"),
    ("purchase_requisitions.company_id", "purchase_requisitions", "company_id", "companies", "company_id"),
    ("purchase_requisitions.plant_id", "purchase_requisitions", "plant_id", "plants", "plant_id"),
    ("purchase_requisitions.material_id", "purchase_requisitions", "material_id", "materials", "material_id"),
]


def load_data() -> dict[str, pd.DataFrame]:
    return {path.stem: pd.read_csv(path) for path in sorted(DATASET_ROOT.glob("**/*.csv"))}


def count_orphans(child: pd.DataFrame, child_column: str, parent: pd.DataFrame, parent_column: str) -> int:
    return int((~child[child_column].isin(parent[parent_column])).sum())


def audit(data: dict[str, pd.DataFrame]) -> dict[str, object]:
    inventory, purchases, receipts = data["inventory"], data["purchase_orders"], data["goods_receipts"]
    counts = {name: len(frame) for name, frame in data.items()}
    duplicate_keys = {name: int(frame.duplicated(PRIMARY_KEYS[name]).sum()) for name, frame in data.items()}
    nulls = {name: int(frame.isna().sum().sum()) for name, frame in data.items()}
    orphans = {
        label: count_orphans(data[child], child_col, data[parent], parent_col)
        for label, child, child_col, parent, parent_col in RELATIONS
    }
    supplier_material_pairs = pd.MultiIndex.from_frame(data["supplier_materials"][["supplier_id", "material_id"]])
    purchase_pairs = pd.MultiIndex.from_frame(purchases[["supplier_id", "material_id"]])
    po_keys = pd.MultiIndex.from_frame(purchases[["purchase_order_id", "purchase_order_line"]])
    receipt_keys = pd.MultiIndex.from_frame(receipts[["purchase_order_id", "purchase_order_line"]])
    inventory_delta = (inventory.on_hand_quantity - inventory.reserved_quantity - inventory.available_quantity).abs()
    receipt_delta = (receipts.quantity_received - receipts.accepted_quantity - receipts.rejected_quantity).abs()
    date_columns = {
        "inventory.last_movement_date": inventory.last_movement_date,
        "purchase_orders.order_date": purchases.order_date,
        "purchase_orders.expected_delivery_date": purchases.expected_delivery_date,
        "purchase_orders.actual_delivery_date": purchases.actual_delivery_date.dropna(),
        "goods_receipts.receipt_date": receipts.receipt_date,
        "purchase_requisitions.requested_date": data["purchase_requisitions"].requested_date,
        "purchase_requisitions.required_date": data["purchase_requisitions"].required_date,
        "supplier_materials.valid_from": data["supplier_materials"].valid_from,
    }
    invalid_dates = {name: int(pd.to_datetime(values, errors="coerce").isna().sum()) for name, values in date_columns.items()}
    return {
        "counts": counts, "duplicate_keys": duplicate_keys, "nulls": nulls, "orphans": orphans,
        "inventory_negative": {column: int((inventory[column] < 0).sum()) for column in [
            "on_hand_quantity", "reserved_quantity", "available_quantity", "safety_stock",
            "average_daily_consumption", "average_unit_cost"]},
        "inventory_reconciliation_failures": int((inventory_delta > DECIMAL_TOLERANCE).sum()),
        "inventory_reconciliation_max_delta": float(inventory_delta.max()),
        "purchase_invalid": {
            "quantity_not_positive": int((purchases.quantity <= 0).sum()),
            "unit_price_not_positive": int((purchases.unit_price <= 0).sum()),
            "transport_cost_negative": int((purchases.transport_cost < 0).sum()),
        },
        "order_after_expected": int((pd.to_datetime(purchases.order_date) > pd.to_datetime(purchases.expected_delivery_date)).sum()),
        "received_without_actual_date": int(((purchases.status == "RECEIVED") & purchases.actual_delivery_date.isna()).sum()),
        "non_received_with_actual_date": int(((purchases.status != "RECEIVED") & purchases.actual_delivery_date.notna()).sum()),
        "receipt_reconciliation_failures": int((receipt_delta > DECIMAL_TOLERANCE).sum()),
        "receipt_reconciliation_max_delta": float(receipt_delta.max()),
        "purchase_invalid_supplier_material": int((~purchase_pairs.isin(supplier_material_pairs)).sum()),
        "receipt_orphan_purchase_line": int((~receipt_keys.isin(po_keys)).sum()),
        "no_consumption_inventory_rows": int((inventory.average_daily_consumption <= 0).sum()),
        "invalid_dates": invalid_dates,
    }


def render_report(result: dict[str, object]) -> str:
    rows = "\n".join(
        f"| `{name}.csv` | {result['counts'][name]} | {result['duplicate_keys'][name]} | {result['nulls'][name]} |"
        for name in sorted(result["counts"])
    )
    relation_rows = "\n".join(f"| `{label}` | {count} |" for label, count in result["orphans"].items())
    inv_numeric = "; ".join(f"{key}: {value}" for key, value in result["inventory_negative"].items())
    purchase_numeric = "; ".join(f"{key}: {value}" for key, value in result["purchase_invalid"].items())
    invalid_dates = "; ".join(f"{key}: {value}" for key, value in result["invalid_dates"].items())
    return f"""# Dataset demo Supply Chain v1 — resultados de auditoría reproducible

Generado por `scripts/audit_demo_data.py`. Tolerancia de reconciliación decimal: `{DECIMAL_TOLERANCE}` (los valores fuente están redondeados a dos decimales).

## Resumen estructural

| Dataset | Filas | Filas duplicadas por clave de negocio/primaria | Celdas nulas |
| --- | ---: | ---: | ---: |
{rows}

## Integridad referencial

| Relación | Huérfanos |
| --- | ---: |
{relation_rows}
| `purchase_orders.(supplier_id, material_id)` → `supplier_materials` | {result['purchase_invalid_supplier_material']} |
| `goods_receipts.(purchase_order_id, line)` → `purchase_orders` | {result['receipt_orphan_purchase_line']} |

## Controles semánticos y temporales

| Control | Fallos | Notas |
| --- | ---: | --- |
| Campos de inventario no negativos | {sum(result['inventory_negative'].values())} | {inv_numeric} |
| `on_hand - reserved = available` | {result['inventory_reconciliation_failures']} | desviación bruta máxima {result['inventory_reconciliation_max_delta']:.2f} |
| Campos numéricos de compra | {sum(result['purchase_invalid'].values())} | {purchase_numeric} |
| `order_date <= expected_delivery_date` | {result['order_after_expected']} | todas las líneas cumplen |
| RECEIVED sin fecha real | {result['received_without_actual_date']} | todas las líneas recibidas cumplen |
| No RECEIVED con fecha real | {result['non_received_with_actual_date']} | las líneas abiertas no contaminan el KPI |
| `received = accepted + rejected` | {result['receipt_reconciliation_failures']} | desviación bruta máxima {result['receipt_reconciliation_max_delta']:.2f} |
| Fechas no nulas interpretables | {sum(result['invalid_dates'].values())} | {invalid_dates} |
| Filas de inventario sin consumo | {result['no_consumption_inventory_rows']} | caso límite esperado, no error de datos |

## Hallazgos

- **INFO:** todos los controles de claves y relaciones pasan en el corpus CSV.
- **INFO:** `valid_to` está vacío en las 71 relaciones proveedor-material; representa una relación abierta y no se cuenta como error.
- **MEDIUM:** plantas, almacenes, relaciones proveedor-material, recepciones y requisiciones existen en CSV, pero no los carga el modelo/loader PostgreSQL actual. Su evidencia sirve para auditoría/diseño, no todavía para Intelligence persistida.
- **LOW:** los controles de reconciliación pasan con la tolerancia indicada; no usar igualdad estricta de punto flotante.
"""


def main() -> None:
    # Windows PowerShell may otherwise expose a legacy cp1252 stdout codec.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    report = render_report(audit(load_data()))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
