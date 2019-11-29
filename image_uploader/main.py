from fastapi import FastAPI
from .routers import handler

app = FastAPI(
    title='image-handler',
    description='Microservice for handling images.',
    version='1.0.0',
    openapi_url='/api/v1/openapi.json')


app.include_router(
    handler.router,
    prefix='/api/v1',
    responses={404: {'description': 'Not found'}},
)
