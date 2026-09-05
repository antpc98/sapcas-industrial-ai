# Dataset demo Supply Chain v1 — resultados de auditoría reproducible

Generado por `scripts/audit_demo_data.py`. Tolerancia de reconciliación decimal: `0.011` (los valores fuente están redondeados a dos decimales).

## Resumen estructural

| Dataset | Filas | Filas duplicadas por clave de negocio/primaria | Celdas nulas |
| --- | ---: | ---: | ---: |
| `companies.csv` | 1 | 0 | 0 |
| `goods_receipts.csv` | 255 | 0 | 0 |
| `inventory.csv` | 35 | 0 | 0 |
| `materials.csv` | 35 | 0 | 14 |
| `plants.csv` | 1 | 0 | 0 |
| `purchase_orders.csv` | 260 | 0 | 5 |
| `purchase_requisitions.csv` | 31 | 0 | 0 |
| `supplier_materials.csv` | 71 | 0 | 71 |
| `suppliers.csv` | 12 | 0 | 0 |
| `warehouses.csv` | 3 | 0 | 0 |

## Integridad referencial

| Relación | Huérfanos |
| --- | ---: |
| `plants.company_id` | 0 |
| `warehouses.plant_id` | 0 |
| `supplier_materials.supplier_id` | 0 |
| `supplier_materials.material_id` | 0 |
| `inventory.plant_id` | 0 |
| `inventory.warehouse_id` | 0 |
| `inventory.material_id` | 0 |
| `purchase_orders.company_id` | 0 |
| `purchase_orders.plant_id` | 0 |
| `purchase_orders.supplier_id` | 0 |
| `purchase_orders.material_id` | 0 |
| `purchase_requisitions.company_id` | 0 |
| `purchase_requisitions.plant_id` | 0 |
| `purchase_requisitions.material_id` | 0 |
| `purchase_orders.(supplier_id, material_id)` → `supplier_materials` | 0 |
| `goods_receipts.(purchase_order_id, line)` → `purchase_orders` | 0 |

## Controles semánticos y temporales

| Control | Fallos | Notas |
| --- | ---: | --- |
| Campos de inventario no negativos | 0 | on_hand_quantity: 0; reserved_quantity: 0; available_quantity: 0; safety_stock: 0; average_daily_consumption: 0; average_unit_cost: 0 |
| `on_hand - reserved = available` | 0 | desviación bruta máxima 0.01 |
| Campos numéricos de compra | 0 | quantity_not_positive: 0; unit_price_not_positive: 0; transport_cost_negative: 0 |
| `order_date <= expected_delivery_date` | 0 | todas las líneas cumplen |
| RECEIVED sin fecha real | 0 | todas las líneas recibidas cumplen |
| No RECEIVED con fecha real | 0 | las líneas abiertas no contaminan el KPI |
| `received = accepted + rejected` | 0 | desviación bruta máxima 0.01 |
| Fechas no nulas interpretables | 0 | inventory.last_movement_date: 0; purchase_orders.order_date: 0; purchase_orders.expected_delivery_date: 0; purchase_orders.actual_delivery_date: 0; goods_receipts.receipt_date: 0; purchase_requisitions.requested_date: 0; purchase_requisitions.required_date: 0; supplier_materials.valid_from: 0 |
| Filas de inventario sin consumo | 1 | caso límite esperado, no error de datos |

## Hallazgos

- **INFO:** todos los controles de claves y relaciones pasan en el corpus CSV.
- **INFO:** `valid_to` está vacío en las 71 relaciones proveedor-material; representa una relación abierta y no se cuenta como error.
- **MEDIUM:** plantas, almacenes, relaciones proveedor-material, recepciones y requisiciones existen en CSV, pero no los carga el modelo/loader PostgreSQL actual. Su evidencia sirve para auditoría/diseño, no todavía para Intelligence persistida.
- **LOW:** los controles de reconciliación pasan con la tolerancia indicada; no usar igualdad estricta de punto flotante.
