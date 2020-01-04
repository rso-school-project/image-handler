from sqlalchemy.orm import Session

from . import models


def get_images(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Image).offset(skip).limit(limit).all()


def get_images_by_user(db: Session, user_id: int):
    return db.query(models.Image).filter(models.Image.user_id == user_id).all()

def get_image_by_id(db: Session, image_id: int):
    return db.query(models.Image).filter(models.Image.id == image_id).first()
