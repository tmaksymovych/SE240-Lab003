from pydantic import BaseModel

class visitorDTO(BaseModel):
    id: int
    name: str
    email: str
    