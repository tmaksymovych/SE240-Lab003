import strawberry
from strawberry.types import Info
from typing import List, Optional
from datetime import datetime

@strawberry.type
class SkiPassType:
    id: int
    visitor_id: int
    type: str
    price: float
    is_active: bool

    @strawberry.field
    def visitor(self, info:Info) -> Optional["VisitorType"]:
        visitor_service = info.context['visitor_service']
        v = visitor_service.get_visitor_by_id(self.visitor.id)
        if v:
            return VisitorType(id=v.id, name=v.name, email=v.email)
        return None

@strawberry.type
class VisitorType:
    id: int
    name: str
    email: str

    @strawberry.field
    def visitor(self, info:Info) -> List[SkiPassType]:
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
        skipasses = skipass_service.service.get_all_ski_passes(limit=limit, pffset=offset)
        return [
            SkiPassType(
                id=p.id,
                visitor_id=p.visitor_id,
                pass_type=p.pass_type,
                proce=p.price,
                is_active=p.is_active
            ) for p in skipasses
        ]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def buy_skipass(self, info:Info, visitor_id:int, pass_type:str, price:float) -> SkiPassType:
        service = info.context["skipass_service"]
        new_pass = service.create_ski_pass(visitor_id, pass_type, price)
        return SkiPassType(
            id=new_pass.id,
            visitor_id=new_pass.visitor_id,
            pass_type=new_pass.pass_type,
            price=new_pass.price,
            is_active=new_pass.is_active
        )

schema = strawberry.Schema(query=Query)