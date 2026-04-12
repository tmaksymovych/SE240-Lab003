from sqlalchemy.orm import Session
from model.models import Visitor
from model.dto.visitor_dto import VisitorDTO

class VisitorService:
    def __init__(self, db: Session):
        self.db = db

    def get_visitor_by_id(self, visitor_id: str) -> VisitorDTO:
        db_visitor = self.db.query(Visitor).filter(Visitor.id == visitor_id).first()
        return VisitorDTO.model_validate(db_visitor)
    
    def create_visitor(self, name: str, email: str) -> VisitorDTO:
        import uuid

        new_visitor = Visitor(
            id=str(uuid.uuid4())[:8],
            name=name,
            email=email
        )
        self.db.add(new_visitor)
        self.db.commit()
        self.refresh(new_visitor)
        return VisitorDTO.model_validate(new_visitor)
