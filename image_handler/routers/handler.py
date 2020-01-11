import time

from typing import List
from fastapi import APIRouter, Depends, Header
from starlette.requests import Request
from func_timeout import func_set_timeout
from sqlalchemy.orm import Session
import requests
import graphene
from starlette.graphql import GraphQLApp

from image_handler import settings
from image_handler.utils import fallback
from image_handler.database import crud, models, schemas, get_db, engine



# models.Base.metadata.create_all(bind=engine, checkfirst=True)
router = APIRouter()


@router.get('/settings')
async def test_configs():
    return {"Config for X:": f"{settings.config_x}", "Config for Y:": f"{settings.comments_disabled}"}


@router.get('/images', response_model=List[schemas.Image])
def read_images(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    images = crud.get_images(db, skip=skip, limit=limit)
    return images


@router.get('/images/user/{user_id}')
def read_user_images(request: Request, user_id: int, db: Session = Depends(get_db)):
    unique_log_id = request.headers.get("unique_log_id", "")

    images = crud.get_images_by_user(db, user_id)

    # Get image comments.
    try:
        if settings.comments_disabled:
            raise
        comments = []
        for image in images:
            res = requests.get('http://image-comments-service:8001/api/v1/comments/image/' + str(image.id), headers={'unique_log_id': unique_log_id})
            res.raise_for_status()
            comments.append(res.json())
    except:
        comments = None
    
    # Get shared users.
    try:
        share = []
        for image in images:
            res = requests.get('http://image-sharing-service:8003/api/v1/share/image/' + str(image.id), headers={'unique_log_id': unique_log_id})
            res.raise_for_status()
            share.append(res.json())
    except:
        share = None

    return { "images": images, "comments": comments, "share": share }


@router.get('/shared-images/user/{user_id}')
def read_user_images(request: Request, user_id: int, db: Session = Depends(get_db)):
    unique_log_id = request.headers.get("unique_log_id", "")
    # Get images shared by this user.
    res = requests.get('http://image-sharing-service:8003/api/v1/share/user/' + str(user_id), headers={'unique_log_id': unique_log_id})
    res.raise_for_status()
    shared = res.json()

    # Retrieve corresponding image records.
    images = []
    for share in shared:
        image = crud.get_image_by_id(db, share["image_id"])
        if image:
            images.append(image)

    # Get image comments.
    try:
        if settings.comments_disabled:
            raise
        comments = []
        for image in images:
            res = requests.get('http://image-comments-service:8001/api/v1/comments/image/' + str(image.id), headers={'unique_log_id': unique_log_id})
            res.raise_for_status()
            comments.append(res.json())
    except:
        comments = None

    return { "images": images, "comments": comments }


def test_fallback():
    return {'Detail': 'This is fallback function. Request timed-out'}


@router.get('/timeout/{seconds}')
@fallback(fallback_function=test_fallback)
@func_set_timeout(3)
def test_timeout_feature(seconds: str):
    time.sleep(float(seconds))
    return {'Timeout': seconds, 'Detail': 'Request did not time-out.'}
