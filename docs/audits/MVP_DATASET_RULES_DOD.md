# Auditoría de dataset Supply Chain y reglas de negocio MVP v1 — Cierre

## Tarea y contexto de planificación

**Tarea:** auditar el dataset demo de Supply Chain y definir las reglas MVP de Inventory, Procurement y Supplier Intelligence. No es una auditoría completa de los datos industriales de SAPCAS. **Estimación original:** 6h. El análisis funcional previo (~1.5h) cubrió contexto, propósito, alcance y selección inicial de reglas; es contexto de planificación, no una medición exacta de ingeniería.

## Trabajo completado

- Se añadió la auditoría reproducible [`scripts/audit_demo_data.py`](../../scripts/audit_demo_data.py).
- Se auditaron los diez CSV para claves de negocio, duplicados, nulos, relaciones, valores numéricos, fechas y reconciliaciones.
- Se formalizaron las 15 reglas acordadas con fuente, dato origen frente a calculado, fórmula, período, cobertura, casos límite, configuración, evidencia, acción y limitaciones.
- Se cerraron las decisiones funcionales de INV-003, PROC-002, SUP-002 y SUP-004 sin ampliar modelos, loaders, endpoints o servicios.
- Se delimitó el alcance a Supply Chain Intelligence v1 y se documentó la estrategia de laboratorios externos sin integrarlos.

## Evidencias obtenidas

| Evidencia | Resultado |
| --- | --- |
| [Script de auditoría](../../scripts/audit_demo_data.py) | Ejecutable y cubierto por test |
| [Resultados de auditoría](MVP_DATASET_AUDIT_RESULTS.md) | 10 CSV, 704 filas, 0 duplicados de claves, 0 referencias huérfanas |
| Controles numéricos y temporales | 0 fallos; reconciliación dentro de tolerancia 0.011 |
| Casos límite | 1 fila sin consumo, tratada como `NO_CONSUMPTION` |
| Relaciones empresariales | 71 relaciones proveedor-material; 260 pares de compra válidos; 255 recepciones enlazadas |
| Reglas y trazabilidad | [04_BUSINESS_RULES.md](../04_BUSINESS_RULES.md), 15 definiciones MVP con ejemplos demo |
| Tests | `pytest -q`: 4 tests correctos |

## Hallazgos

- **INFO:** el corpus CSV de Supply Chain es internamente coherente para el alcance auditado.
- **INFO:** `valid_to` está vacío en las 71 relaciones proveedor-material y se interpreta como vigencia abierta.
- **LOW:** los importes están redondeados a dos decimales; las reconciliaciones necesitan tolerancia 0.011, no igualdad estricta de `float`.
- **MEDIUM:** plantas, almacenes, relaciones proveedor-material, recepciones y requisiciones existen en CSV, pero todavía no se persisten en PostgreSQL. Es una limitación de implementación, no de definición funcional del MVP.
- **INFO:** los scores de calidad y fiabilidad del maestro son datos fuente; la tasa de aceptación es una métrica SAPCAS calculada y ambas se mantienen separadas.

## Decisiones funcionales cerradas

| Regla | Decisión cerrada |
| --- | --- |
| INV-003 | Usa plazo del proveedor preferente elegible único; si no existe, mínimo plazo elegible, con base de selección explicable. Sin plazo, aplica la condición de safety stock y declara `NOT_AVAILABLE`. |
| PROC-002 | `current_price` es la última compra RECEIVED; histórico son compras RECEIVED anteriores dentro de ventana configurable, con mínimo de 3 observaciones. +10 % es alerta demo `MEDIUM` configurable. |
| SUP-002 | El MVP demo calcula aceptación directamente desde `goods_receipts.csv`, con ventana configurable, cobertura visible y estados `NOT_CALCULABLE`/`INSUFFICIENT_DATA`. |
| SUP-004 | Elegibilidad, escalas iniciales comparables, requisitos de cobertura, manejo de faltantes y empate están definidos; ranking solo entre elegibles y siempre explicable. |

## Trabajo futuro de implementación — no bloquea este Step

- Modelos SQLAlchemy, migraciones, loaders y persistencia de plantas, almacenes, relaciones proveedor-material, recepciones y requisiciones.
- Servicios, endpoints, interfaz y ejecución productiva de las reglas.
- Calibración de umbrales/pesos con piloto y datos de cliente; no es condición para que la semántica MVP quede definida.
- ML, forecasting, optimización, agentes LLM, C-MAPSS, Cognite y los demás laboratorios.

## Checklist DoD

| Requisito | Estado |
| --- | --- |
| Dataset Supply Chain auditado y reproducible | Completo |
| Relaciones, gaps y campos relevantes identificados | Completo |
| Reglas Inventory, Procurement y Supplier definidas | Completo |
| Fórmulas, inputs, periodos, edge cases y configuración trazables | Completo |
| Fuente frente a dato calculado distinguido | Completo |
| Recomendación explicable y sin puntuaciones inventadas | Completo |
| Scope Supply Chain v1 y laboratorios externos diferenciados | Completo |
| Documentación versionada y tests | Completo |

## Evaluación final: DONE

**DONE significa que el dataset Supply Chain v1 está auditado y las reglas MVP están funcionalmente definidas.** No significa que el producto esté implementado, que los umbrales estén calibrados industrialmente, ni que los demás dominios de SAPCAS estén auditados.

No quedan decisiones funcionales bloqueantes para este Step. **Esfuerzo restante para el Step: 0h.** Las tareas de implementación y calibración se estimarán en Steps posteriores.
