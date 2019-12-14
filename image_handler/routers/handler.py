import time

from fastapi import APIRouter
from func_timeout import func_set_timeout

from image_handler import settings
from image_handler.utils import fallback

router = APIRouter()


@router.get('/settings')
async def test_configs():
    return {"Config for X:": f"{settings.config_x}", "Config for Y:": f"{settings.config_y}"}


def image_generator():
    return [{'id': index, 'name': "image" + str(index), 'path': "/path/" + str(index)} for index in range(1, 6)]


@router.get('/images')
def list_images():
    return image_generator()


def test_fallback():
    return {'Detail': 'This is fallback function. Request timed-out'}


@router.get('/timeout/{seconds}')
@fallback(fallback_function=test_fallback)
@func_set_timeout(3)
def test_timeout_feature(seconds: str):
    time.sleep(float(seconds))
    return {'Timeout': seconds, 'Detail': 'Request did not time-out.'}
