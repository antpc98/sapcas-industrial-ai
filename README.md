# SAPCAS Industrial AI

SAPCAS Industrial AI es un MVP B2B para empresas industriales. Convierte datos de materiales, inventario, compras y proveedores en indicadores, reglas y, progresivamente, recomendaciones para reducir costes y mejorar decisiones.

**Estado actual:** base de datos, carga demo y API de consulta implementadas. Las reglas de Intelligence y las recomendaciones aún no lo están.

## Inicio rápido

Requisitos: Python y Docker/Docker Compose.

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

```bash
pip install -r requirements.txt
docker compose up -d db
alembic upgrade head
python scripts/load_demo_data.py
uvicorn app.main:app --reload
```

La URL por defecto es `postgresql+psycopg://sapcas:sapcas@localhost:5432/sapcas`, coherente con `docker-compose.yml`. Puede sobrescribirse con `DATABASE_URL` en `.env`; hoy no existe `.env.example`.

Swagger: `http://localhost:8000/docs`. Healthcheck: `GET /health` devuelve `{"status": "healthy"}`.

## Endpoints disponibles

| Método | Ruta | Función |
| --- | --- | --- |
| GET | `/health` | Healthcheck |
| GET | `/api/v1/` | Metadatos de API |
| GET | `/api/v1/materials` | Materiales |
| GET | `/api/v1/suppliers` | Proveedores |
| GET | `/api/v1/inventory` | Stock por ubicación |
| GET | `/api/v1/purchases` | Líneas de pedido |

Son endpoints de lectura; no calculan aún riesgos, KPIs ni recomendaciones.

## Stack y lectura recomendada

Python, FastAPI, PostgreSQL, SQLAlchemy, Alembic, Pydantic, Pandas, pytest y Docker Compose. El MVP evita Redis, Kafka, Kubernetes, Terraform, LangChain y arquitectura distribuida.

Empieza por [contexto](docs/00_PROJECT_CONTEXT.md), sigue con [arquitectura](docs/01_ARCHITECTURE.md), [modelo](docs/02_DATA_MODEL.md) y [dataset](docs/03_DATASET.md). Consulta después [reglas](docs/04_BUSINESS_RULES.md), [alcance](docs/05_MVP_SCOPE.md), [roadmap](docs/06_ROADMAP.md), [decisiones](docs/07_DECISIONS.md) y [laboratorios futuros](docs/08_LABS.md).
