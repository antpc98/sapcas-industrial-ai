from pydantic import BaseModel, ConfigDict


class MaterialRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    code: str
    description: str
    material_group: str
    material_type: str
    base_unit: str
    criticality: str
    certification_required: str | None
    active: bool
