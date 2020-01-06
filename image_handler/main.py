from fastapi import FastAPI
from starlette_prometheus import metrics, PrometheusMiddleware
from starlette.requests import Request
#from starlette.middleware.cors import CORSMiddleware

import graphene
from starlette.graphql import GraphQLApp
from image_handler.database import crud, get_db

from . import VERSION, PREFIX
from .routers import handler
from .utils import check_liveness, check_readiness

from image_handler.logger import logger

app = FastAPI(
    title='image-handler',
    description='Microservice for handling images.',
    version=VERSION,
    # openapi_url=f'/image-handler{PREFIX}/openapi.json',
)

# origins = [
#     "http://localhost",
#     "http://localhost:3000",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

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


class Image(graphene.ObjectType):
    id = graphene.Int()
    user_id = graphene.Int()
    file_name = graphene.String()
    file_hash = graphene.String()
    tags = graphene.String()

class Query(graphene.ObjectType):
    images = graphene.List(Image, user_id=graphene.Int(default_value=None))

    def resolve_images(self, context, **kwargs):
        user_id = kwargs.get('user_id')

        if user_id is not None:
            # Get images of some user.
            return crud.get_images_by_user(next(get_db()), user_id)

        # Get all images.
        return crud.get_images(next(get_db()))

app.add_route("/graphql/", GraphQLApp(schema=graphene.Schema(query=Query)))