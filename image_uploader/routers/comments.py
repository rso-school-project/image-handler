import uuid


from fastapi import APIRouter
from image_comments import settings

router = APIRouter()


@router.get("/")
async def test_configs():
    return {"Config for X:": f"{settings.config_x}",
            "Config for Y:": f"{settings.config_y}"}


def comment_generator():
    return [{'id': index, 'author_id': uuid.uuid1(), 'text': 'Test comment ' + str(index)} for index in range(1, 6)]


@router.get("/comments/")
async def list_comments():
    return comment_generator()
