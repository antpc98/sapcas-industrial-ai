# Dataset demo

`datasets/demo/` es sintético y representa a Guadalquivir Precision Systems S.L., una empresa ficticia metal-mecánica/auxiliar aeroespacial de Sevilla. Sirve para pruebas y demos, no para describir una empresa real.

## Datos maestros

| CSV | Filas | Representa | Carga actual |
| --- | ---: | --- | --- |
| `companies.csv` | 1 | Empresa | Sí, Company |
| `materials.csv` | 35 | Materiales | Sí, Material |
| `suppliers.csv` | 12 | Proveedores y scores demo | Sí, Supplier |
| `plants.csv` | 1 | Centro productivo | No, no modelado |
| `warehouses.csv` | 3 | Almacén lógico | No, no modelado |
| `supplier_materials.csv` | 71 | Proveedor-material, precio, MOQ, lead time, certificación | No, no modelado |

MOQ es la cantidad mínima de pedido; lead time, el plazo hasta entrega/disponibilidad.

## Datos transaccionales

| CSV | Filas | Representa | Carga actual |
| --- | ---: | --- | --- |
| `inventory.csv` | 35 | Stock por planta, almacén y material | Sí, InventoryItem |
| `purchase_orders.csv` | 260 | Líneas históricas y abiertas de pedido | Sí, Purchase |
| `purchase_requisitions.csv` | 31 | Necesidades internas previas a pedido | No, no modelado |
| `goods_receipts.csv` | 255 | Recepciones, aceptaciones y rechazos | No, no modelado |

Un *goods receipt* es la recepción física de mercancía. Inventario aporta cobertura y valor potenciales; pedidos, histórico de precio y entrega. `supplier_materials`, `goods_receipts` y requisiciones serán claves para elegibilidad, calidad y urgencia. Los escenarios de `documentation/known_scenarios.md` son expectativas de reglas futuras, no resultados calculados.

El loader procesa solo los cinco CSV marcados como cargados y es repetible: actualiza por ID de maestro, ubicación-material o pedido-línea.

La evidencia estructural, semántica y relacional del corpus se genera con
[`scripts/audit_demo_data.py`](../scripts/audit_demo_data.py) y queda versionada en
[`audits/MVP_DATASET_AUDIT_RESULTS.md`](audits/MVP_DATASET_AUDIT_RESULTS.md).
