# Contexto del proyecto

## Propósito

Las empresas industriales deciden sobre compras e inventario a partir de datos dispersos: materiales disponibles, consumo, coste y proveedores. SAPCAS Industrial AI busca convertir esos datos en información accionable para reducir coste de compra, evitar faltantes y limitar capital inmovilizado.

El usuario inicial es el equipo de compras, aprovisionamiento o inventario. No es un chatbot generalista: los datos y reglas empresariales deben ser la fuente de verdad; una capa generativa futura solo podría explicar resultados.

```text
Datos operativos → normalización → KPIs y reglas → riesgos/oportunidades → recomendaciones
```

El dominio en construcción es **Supply Chain Intelligence v1**: Inventory Intelligence, Procurement Intelligence, Supplier Intelligence y posteriormente RFQ. RFQ (*request for quotation*) es una solicitud de oferta a proveedores. SAPCAS Industrial AI evolucionará después con dominios de mantenimiento, producción, operaciones, calidad/scrap, coste/pérdidas y decisión transversal; no forman parte de esta auditoría.

## Estado

### DONE

- Modelos PostgreSQL: Company, Material, Supplier, InventoryItem y Purchase.
- Migración inicial, API FastAPI de lectura y healthcheck.
- Dataset sintético y carga repetible con Pandas + SQLAlchemy para esos cinco dominios.

### IN PROGRESS

- Las reglas MVP de Supply Chain v1 están definidas y auditadas; no existen aún servicios ni endpoints que las calculen.

### PLANNED

- Inventory: cobertura, rotura, sobrestock, inmovilizado y baja rotación.
- Procurement: precios, coste efectivo y cumplimiento de entrega.
- Supplier: desempeño, calidad, elegibilidad y ranking.
- RFQ/recomendaciones y demo comercial.

## Límites y siguiente objetivo

No se pretende construir un ERP, mantenimiento, planificación de producción, visión artificial, trading, integraciones específicas sin cliente ni infraestructura distribuida. El siguiente objetivo es implementar de forma incremental las reglas Supply Chain v1 ya definidas, manteniendo su trazabilidad a datos origen.
