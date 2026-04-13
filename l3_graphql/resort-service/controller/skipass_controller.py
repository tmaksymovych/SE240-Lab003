from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from service.skipass_service import SkiPassService
from model.dto.skipass_dto import SkiPassDTO
from typing import List

router = APIRouter(prefix="/skipasses", tags=["Ski Passes"])

@router.post("/buy", response_model=SkiPassDTO)
def buy_pass(visitor_id: str, pass_type: str, price: float, db: Session = Depends(get_db)):
    service = SkiPassService(db)
    return service.create_ski_pass(visitor_id, pass_type, price)

@router.get("/", response_model=List[SkiPassDTO])
def list_passes(
    limit: int = Query(10, ge=1), 
    offset: int = Query(0, ge=0), 
    db: Session = Depends(get_db)
):
    service = SkiPassService(db)
    return service.get_all_ski_passes(limit, offset)