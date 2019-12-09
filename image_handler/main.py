from fastapi import FastAPI
from starlette_prometheus import metrics, PrometheusMiddleware

from .routers import handler

VERSION = '1.0.0'
API_VERSION = 'v1'
PREFIX = f'/api/{API_VERSION}/images'

app = FastAPI(
    title='image-handler',
    description='Microservice for handling images.',
    version=VERSION,
    openapi_url=f'{PREFIX}/openapi.json',
)

app.add_middleware(PrometheusMiddleware)
app.add_route(f'{PREFIX}/metrics/', metrics)

app.include_router(
    handler.router, prefix=PREFIX, responses={404: {'description': 'Not found'}},
)
