from fastapi import FastAPI, Depends

from database import get_db
from sqlalchemy.orm import Session

from service.visitor_service import SkiPassService
from service.skipass_service import VisitorService

app = FastAPI( title="Awesome Resort app", description="GraphQl for Ski REsort Manager", version="0.1.0")

import strawberry.fastapi
from graphqlapi.schema import schema

def get_graphql_context(db: Session=Depends(get_db)):
    return {
        "skipass_service": SkiPassService(db),
        "visitor_service": VisitorService(db)
        }

graphql_app = strawberry.fastapi.GraphQLRouter(
    schema=schema, 
    context_getter=get_graphql_context)

app.include_router(graphql_app, prefix="/graphql", tags=["graphql"])