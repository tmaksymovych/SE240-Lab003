from fastapi import FastAPI, Depends
from controller.notes_controller import router as notes_router

from service.visitor_service import get_skipass_service
from service.skipass_service import get_visitor_service

app = FastAPI( title="Awesome Resort app", description="GraphQl for Ski REsort Manager", version="0.1.0")
app.include_router(notes_router)

import strawberry.fastapi
from graphqlapi.schema import schema

def get_graphql_context( 
                        skipass_service = Depends(get_skipass_service),
                        visitor_service = Depends(get_visitor_service)
                        ):
    return {"skipass_service": skipass_service, "visitor_service": visitor_service}

graphql_app = strawberry.fastapi.GraphQLRouter(
    schema=schema, 
    context_getter=get_graphql_context)
app.include_router(graphql_app, prefix="/graphql", tags=["graphql"])