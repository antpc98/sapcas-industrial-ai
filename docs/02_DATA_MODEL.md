# Modelo de datos actual

Solo los modelos siguientes están persistidos por la migración inicial.

```text
Company (1) ──< Purchase >── (1) Supplier
                    |
                    └──────── (1) Material ──< InventoryItem

Plant y Warehouse son identificadores, no modelos relacionales.
```

## Company — `companies`

Empresa propietaria de la operación. PK: `company_id` (atributo `id`). Nombre, país, moneda, industria y notas. Se relaciona con Purchase y será ámbito de indicadores. Sin endpoint actual.

## Material — `materials`

Producto, componente o materia prima. PK `material_id`; `material_code` único. Incluye descripción, grupo/tipo, unidad base, criticidad, certificación y activo. Se relaciona con compras e inventario; será el eje de cobertura, coste y riesgo.

## Supplier — `suppliers`

Proveedor. PK `supplier_id`; `supplier_code` único. Incluye país, moneda, pago, `reliability_score`, `quality_score` y activo. Se relaciona con Purchase. Los scores son datos demo: hoy no se calculan ni interpretan.

## InventoryItem — `inventory_items`

Stock de material por ubicación. PK técnica `id`; unicidad por planta, almacén y material; solo material es FK. Guarda stock físico, reservado, disponible, seguridad, consumo medio diario, coste medio y último movimiento. Fuente prevista de Inventory Intelligence.

## Purchase — `purchases`

Línea de pedido histórica o abierta. PK técnica `id`; unicidad por pedido y línea. FK a Company, Supplier y Material; planta no tiene FK. Guarda fechas, cantidad, precio, moneda, transporte y estado. Fuente prevista para precio, coste y entrega.

Plantas, almacenes, relación proveedor-material, recepciones y requisiciones existen en CSV, pero no están modelados ni expuestos.
