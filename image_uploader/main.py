from fastapi import FastAPI
from .routers import comments

app = FastAPI(
    title='image-comments',
    description='Microservice for handling image comments',
    version='1.0.0',
    openapi_url='/api/v1/openapi.json')


app.include_router(
    comments.router,
    prefix='/api/v1',
    responses={404: {'description': 'Not found'}},
)
