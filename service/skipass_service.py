from sqlalchemy.orm import Session
from model.models import SkiPass
from model.dto.skipass_dto import SkiPassDTO
from typing import List

class SkiPassService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_ski_passes(self, limit: int, offset: int) -> List[SkiPassDTO]:
        db_passes = self.db.query(SkiPass).offset(offset).limit(limit).all()
        return [SkiPassDTO.model_validate(passes) for passes in db_passes]
    
    def get_passes_by_visitor(self, visitor_id: str) -> List[SkiPassDTO]:
        db_passes = self.db.query(SkiPass).filter(SkiPass.visitor_id == visitor_id).all()
        return [SkiPassDTO.model_validate(passes) for passes in db_passes]
    
    def create_skipass(self, visitor_id: str, pass_type: str, price: float) -> SkiPassDTO:
        import uuid
        new_pass = SkiPass(
            id=str(uuid.uuid4())[:8],
            visitor_id=visitor_id,
            pass_type=pass_type,
            price=price,
            is_active=True
        )
        self.db.add(new_pass)
        self.db.commit()
        self.db.refresh(new_pass)
        return SkiPassDTO.model_validate(new_pass)
    