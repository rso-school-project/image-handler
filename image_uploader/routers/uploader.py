from fastapi import APIRouter
from image_uploader import settings

router = APIRouter()


@router.get("/")
async def test_configs():
    return {"Config for X:": f"{settings.config_x}",
            "Config for Y:": f"{settings.config_y}"}


def image_generator():
    return [{'id': index, 'name': "image" + str(index), 'path': "/path/" + str(index)} for index in range(1, 6)]


@router.get("/images/")
async def list_images():
    return image_generator()
