import time

from typing import List
from fastapi import APIRouter, Depends
from starlette.requests import Request
from func_timeout import func_set_timeout
from sqlalchemy.orm import Session

from image_handler import settings
from image_handler.utils import fallback
from image_handler.database import crud, models, schemas, get_db, engine


# models.Base.metadata.create_all(bind=engine, checkfirst=True)
router = APIRouter()


@router.get('/settings')
async def test_configs():
    return {"Config for X:": f"{settings.config_x}", "Config for Y:": f"{settings.config_y}"}


@router.get('/images', response_model=List[schemas.Image])
def read_images(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # NOTE: this is importat for logging.
    #       we get unique_log_id as a header in request object.
    #       unique_log_id = request.header.get('unique_log_id')
    #       Use this log id, when calling another microservice from here.
    images = crud.get_images(db, skip=skip, limit=limit)
    return images


@router.get('/images/user/{user_id}', response_model=List[schemas.Image])
def read_user_images(user_id: int, db: Session = Depends(get_db)):
    # NOTE: this is importat for logging.
    #       we get unique_log_id as a header in request object.
    #       unique_log_id = request.header.get('unique_log_id')
    #       Use this log id, when calling another microservice from here.
    images = crud.get_images_by_user(db, user_id)
    return images


def test_fallback():
    return {'Detail': 'This is fallback function. Request timed-out'}


@router.get('/timeout/{seconds}')
@fallback(fallback_function=test_fallback)
@func_set_timeout(3)
def test_timeout_feature(seconds: str):
    time.sleep(float(seconds))
    return {'Timeout': seconds, 'Detail': 'Request did not time-out.'}
