# Data Dictionary v0.1

## Datos maestros

### companies.csv
- `company_id`: identificador interno.
- `company_name`: nombre de empresa.
- `country`: ISO país.
- `currency`: divisa principal.
- `industry`: vertical industrial.

### plants.csv
Centro productivo perteneciente a una empresa.

### warehouses.csv
Almacén lógico dentro de una planta.

### materials.csv
Maestro de materiales.
- `material_id`: clave interna.
- `material_code`: referencia de negocio.
- `material_group`: familia.
- `material_type`: RAW_MATERIAL / COMPONENT / CONSUMABLE.
- `base_unit`: unidad base.
- `criticality`: LOW / MEDIUM / HIGH / CRITICAL.
- `certification_required`: requisito documental simplificado.

### suppliers.csv
Maestro de proveedores con términos básicos y scores demo.

### supplier_materials.csv
Relación proveedor-material.
Contiene precio actual, MOQ, cantidad estándar, lead time y disponibilidad de certificado.

## Transacciones

### inventory.csv
Stock por planta, almacén y material.
- `on_hand_quantity`: físico.
- `reserved_quantity`: comprometido.
- `available_quantity`: disponible.
- `average_daily_consumption`: consumo medio diario.
- `average_unit_cost`: coste medio.
- `last_movement_date`: último movimiento conocido.

### purchase_requisitions.csv
Necesidades de compra previas a pedido.

### purchase_orders.csv
Líneas históricas y abiertas de pedidos de compra.

### goods_receipts.csv
Recepciones asociadas a líneas de pedido, incluyendo cantidades aceptadas y rechazadas.

## Regla de diseño
Los datos son sintéticos y se usan para probar lógica, no para representar una empresa concreta.
