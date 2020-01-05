from pydantic import BaseModel


class ImageBase(BaseModel):
    user_id: int


class Image(ImageBase):
    id: int
    file_name: str
    file_hash: str
    tags: str

    class Config:
        orm_mode = True
