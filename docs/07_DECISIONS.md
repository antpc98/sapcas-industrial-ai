# Registro de decisiones

Solo se registran decisiones respaldadas por código o documentación. Fechas no presentes se indican expresamente.

## ADR-001 — MVP con arquitectura sencilla

**Fecha:** no registrada  
**Contexto:** validar valor de negocio.  
**Decisión:** aplicación Python monolítica; sin Redis, Kafka, Kubernetes, Terraform, LangChain ni arquitectura distribuida en el MVP.  
**Motivo:** mantenerlo comprensible, mantenible y demostrable.  
**Consecuencias:** evaluar escala/integraciones cuando se justifiquen.

## ADR-002 — PostgreSQL y Alembic

**Fecha:** 2026-08-18 (migración inicial)  
**Contexto:** persistir el modelo inicial.  
**Decisión:** PostgreSQL con migración Alembic para cinco modelos.  
**Motivo:** configuración Docker Compose, SQLAlchemy y migración versionada existentes.  
**Consecuencias:** aplicar migraciones antes de cargar datos.

## ADR-003 — FastAPI como API inicial

**Fecha:** no registrada  
**Contexto:** exponer datos para desarrollo/demo.  
**Decisión:** FastAPI con `/api/v1` y Pydantic de lectura.  
**Motivo:** implementación actual.  
**Consecuencias:** endpoints actuales son de consulta; Intelligence no debe presentarse como implementada.

## ADR-004 — Carga demo con Pandas y SQLAlchemy

**Fecha:** no registrada  
**Contexto:** cargar CSV sintéticos repetidamente.  
**Decisión:** Pandas, validación de columnas y upsert SQLAlchemy.  
**Motivo:** `scripts/load_demo_data.py`.  
**Consecuencias:** solo cinco CSV llegan hoy a PostgreSQL.

## ADR-005 — Reglas Supply Chain v1 explicables y trazables

**Fecha:** 2026-09-05

**Contexto:** cerrar la definición funcional sin adelantar implementación.

**Decisión:** cada regla declara datos fuente, dato calculado, fórmula, periodo, cobertura, casos límite, configuración, evidencia y acción. Los faltantes se expresan como `NOT_AVAILABLE`, `INSUFFICIENT_DATA` o `NOT_CALCULABLE`; no se inventan puntuaciones.
**Consecuencias:** las reglas quedan funcionalmente definidas; servicios, persistencia y UI son trabajo posterior.

## ADR-006 — Supply Chain v1 y laboratorios externos separados

**Fecha:** 2026-09-05

**Contexto:** evitar presentar el MVP como todo SAPCAS Industrial AI.

**Decisión:** el dataset demo se reserva para Supply Chain; NASA C-MAPSS y Cognite se documentan como LAB01/LAB02 futuros, sin integración.
**Consecuencias:** no se amplía el modelo, infraestructura ni alcance del MVP por datasets externos.
