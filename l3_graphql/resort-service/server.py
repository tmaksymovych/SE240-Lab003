from fastapi import FastAPI, Depends

from database import get_db
from sqlalchemy.orm import Session

from service.visitor_service import VisitorService
from service.skipass_service import SkiPassService

from strawberry.dataloader import DataLoader

from strawberry.fastapi import GraphQLRouter
from strawberry.subscriptions import GRAPHQL_WS_PROTOCOL

from controller.visitor_controller import router as visitor_router
from controller.skipass_controller import router as skipass_router


app = FastAPI( title="Awesome Resort app", description="GraphQl for Ski REsort Manager", version="0.1.0")

app.include_router(visitor_router)
app.include_router(skipass_router)

import strawberry.fastapi
from graphqlapi.schema import schema

def get_graphql_context(db: Session=Depends(get_db)):

    skipass_service = SkiPassService(db)
    visitor_service = VisitorService(db)
    skipass_loader = DataLoader(load_fn=skipass_service.get_skipasses_by_visitor_ids)
    

    return {
        "skipass_service": skipass_service,
        "visitor_service": visitor_service,
        "skipass_loader" : skipass_loader 
        }

graphql_app = strawberry.fastapi.GraphQLRouter(
    schema=schema, 
    context_getter=get_graphql_context)

# app.include_router(graphql_app, prefix="/graphql", tags=["graphql"])

graphql_app = strawberry.fastapi.GraphQLRouter(
    schema=schema,
    context_getter=get_graphql_context
)
app.include_router(graphql_app, prefix="/graphql", tags=["GraphQL"])

@app.get("/")
def root():
    return {"message": "Welcome to the Ski Resort API. Visit /docs for REST or /graphql for GraphQL."}