from pydantic import BaseModel, ConfigDict

class SkiPassDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    visitor_id: str
    type: str
    price: float
    is_active: bool = True