# Arquitectura actual

## Flujo implementado

```text
CSV demo → Pandas + validación mínima → SQLAlchemy → PostgreSQL ← FastAPI → API de lectura
```

`scripts/load_demo_data.py` lee cinco CSV, valida columnas obligatorias y hace inserción/actualización por claves de negocio. Ejecutar `alembic upgrade head` antes de la carga.

Los servicios Intelligence son futuros:

```text
PostgreSQL → servicios/reglas Intelligence (planificado) → KPIs/riesgos/recomendaciones (planificado)
```

| Ubicación | Responsabilidad actual |
| --- | --- |
| `app/api/` | Router `/api/v1` y sesión de BD. |
| `app/core/` | Configuración y motor/sesión SQLAlchemy. |
| `app/models/` | Cinco modelos ORM actuales. |
| `app/schemas/` | Respuestas Pydantic de Material, Supplier, InventoryItem y Purchase. |
| `app/services/`, `app/agents/`, `app/importers/`, `app/context/` | Paquetes creados, sin implementación. La carga está en `scripts/`. |
| `datasets/` | CSV sintéticos y documentación de escenarios. |
| `alembic/` | Configuración y migración inicial. |
| `tests/` | Healthcheck y validador de columnas. |

La API consulta directamente mediante SQLAlchemy, sin capa de servicio intermedia. `plant_id` y `warehouse_id` no tienen modelo ni FK. Company está cargada y persistida, pero no tiene schema ni endpoint.
