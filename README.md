# SAPCAS Industrial AI

**SAPCAS Industrial AI ayuda a empresas industriales a reducir costes de compra e inventario mediante agentes conectados a sus datos operativos.**

## MVP

- Inventory Intelligence
- RFQ Intelligence
- Procurement Intelligence

## Stack inicial

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- Pandas
- pytest
- Docker

> Alcance deliberadamente reducido para la v0.1: sin Redis, Kubernetes, Terraform ni LangChain.

## Ejecución local

### 1. Crear entorno virtual

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Variables de entorno

Copia `.env.example` como `.env`.

### 4. Levantar PostgreSQL

```bash
docker compose up -d db
```

### 5. Ejecutar API

```bash
uvicorn app.main:app --reload
```

### 6. Comprobar healthcheck

```http
GET http://localhost:8000/health
```

Respuesta:

```json
{
  "status": "healthy"
}
```

Swagger:

```text
http://localhost:8000/docs
```

## Estructura

```text
app/
├── api/
├── core/
├── models/
├── schemas/
├── services/
├── agents/
├── importers/
└── context/

datasets/demo/
scripts/
tests/
docs/
alembic/
```

## Objetivo del primer ciclo

Convertir datos de inventario, compras y proveedores en decisiones económicas medibles antes de introducir capas avanzadas de IA.
