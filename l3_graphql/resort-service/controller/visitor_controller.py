from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from service.visitor_service import VisitorService
from model.dto.visitor_dto import VisitorDTO
from typing import List


router = APIRouter(prefix="/visitors", tags=["Visitors"])

@router.post("/", response_model=VisitorDTO)
def register_visitor(name: str, email: str, db: Session = Depends(get_db)):
    service = VisitorService(db)
    return service.create_visitor(name, email)

@router.get("/{visitor_id}", response_model=VisitorDTO)
def get_visitor(visitor_id: str, db: Session = Depends(get_db)):
    service = VisitorService(db)
    visitor = service.get_visitor_by_id(visitor_id)
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    return visitor

@router.put("/{visitor_id}", response_model=VisitorDTO)
def update_visitor(visitor_id: str, name: str, email: str, db: Session = Depends(get_db)):
    service = VisitorService(db)
    updated = service.update_visitor_info(visitor_id, name, email)
    if not updated:
        raise HTTPException(status_code=404, detail="Visitor not found")
    return updated