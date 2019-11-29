from fastapi import FastAPI
from .routers import uploader

app = FastAPI(
    title='image-uploader',
    description='Microservice for uploading images.',
    version='1.0.0',
    openapi_url='/api/v1/openapi.json')


app.include_router(
    uploader.router,
    prefix='/api/v1',
    responses={404: {'description': 'Not found'}},
)
