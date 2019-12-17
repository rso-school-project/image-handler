from fastapi import FastAPI
from starlette_prometheus import metrics, PrometheusMiddleware
from starlette.requests import Request

from . import VERSION, PREFIX
from .routers import handler
from .utils import check_liveness, check_readiness

from image_handler.logger import logger

app = FastAPI(
    title='image-handler',
    description='Microservice for handling images.',
    version=VERSION,
    openapi_url=f'/image-handler{PREFIX}/openapi.json',
)


@app.middleware("http")
async def logger_middleware(request: Request, call_next):
    path = PrometheusMiddleware.get_path_template(request)
    logger.info(f'{path} ENTRY', extra={'unique_log_id': request.headers.get('unique_log_id', 'Not provided')})
    response = await call_next(request)
    logger.info(f'{path} EXIT', extra={'unique_log_id': request.headers.get('unique_log_id', 'Not provided')})
    return response


app.add_middleware(PrometheusMiddleware)
app.add_route('/metrics/', metrics)

app.include_router(
    handler.router, prefix=PREFIX, responses={404: {'description': 'Not found'}},
)

app.add_route('/health/live', check_liveness)
app.add_route('/health/ready', check_readiness)
