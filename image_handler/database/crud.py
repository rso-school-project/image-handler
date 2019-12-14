from sqlalchemy.orm import Session

from . import models


def get_images(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Images).offset(skip).limit(limit).all()


def get_image_by_user(db: Session, user_id: str):
    return db.query(models.Images).filter(models.Images.user_id == user_id).first()
