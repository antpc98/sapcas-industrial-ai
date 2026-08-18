from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")


@router.get("/", tags=["system"])
def api_root() -> dict[str, str]:
    return {
        "service": "SAPCAS Industrial AI",
        "version": "0.1.0",
    }
