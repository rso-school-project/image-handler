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


def image_commnets_fallback():
    return {'default': 'Timeout: comments unavailable'}


@router.get('/')
@fallback(fallback_function=image_commnets_fallback)
@func_set_timeout(3)
async def list_images():
    return image_generator()
