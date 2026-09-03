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
