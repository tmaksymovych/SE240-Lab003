import strawberry
from strawberry.types import Info
from typing import List, Optional
from datetime import datetime

@strawberry.type
class SkiPassType:
    id: str
    visitor_id: str
    pass_type: str
    price: float
    is_active: bool

    @strawberry.field
    def visitor(self, info:Info, visitor_id: str) -> Optional['VisitorType']:
        v_dto = info.context["visitor_service"].get_visitor_by_id(visitor_id)
        if v_dto:
            return VisitorType(id=v_dto.id, name=v_dto.name, email=v_dto.email)
        
@strawberry.type
class VisitorType:
    id: str
    name: str
    email: str

    @strawberry.field
    def skipasses(self, info:Info) -> List[SkiPassType]:
        skipass_service = info.context["skipass_service"]
        passes = skipass_service.get_passes_by_visitor(self.id)
        return [
            SkiPassType(
                id=p.id,
                visitor_id=p.visitor_id,
                pass_type=p.pass_type,
                price=p.price,
                is_active=p.is_active
            ) for p in passes
        ]


@strawberry.type
class Query:
    @strawberry.field
    def visitor(self, info:Info, visitor_id: str) -> Optional[VisitorType]:
        visitor_service = info.context["visitor_service"]
        v = visitor_service.get_visitor_by_id(visitor_id)
        if v:
            return VisitorType(
                id=v.id,
                name=v.name,
                email=v.email
            )
        return None
    
    @strawberry.field
    def all_skipasses(self, info:Info, limit: int=10, offset: int=0) -> List[SkiPassType]:
        skipass_service = info.context["skipass_service"]
        skipasses = skipass_service.get_all_ski_passes(limit=limit, offset=offset)
        return [
            SkiPassType(
                id=p.id,
                visitor_id=p.visitor_id,
                pass_type=p.pass_type,
                price=p.price,
                is_active=p.is_active
            ) for p in skipasses
        ]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def buy_skipass(self, info:Info, visitor_id:str, pass_type:str, price:float) -> SkiPassType:
        service = info.context["skipass_service"]
        return service.create_skipass(visitor_id, pass_type, price)
    
    @strawberry.mutation
    def create_visitor(self, info:Info, name:str, email:str) -> VisitorType:
        service = info.context["visitor_service"]
        return service.create_visitor(name, email)

schema = strawberry.Schema(query=Query, mutation=Mutation)