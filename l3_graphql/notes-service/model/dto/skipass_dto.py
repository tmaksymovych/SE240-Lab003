from pydantic import BaseModel

class SkiPassDTO(BaseModel):
    id: int
    visitor_id: int
    type: str
    price: float
    is_active: bool