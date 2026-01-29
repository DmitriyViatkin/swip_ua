from pydantic import BaseModel

class FavoriteBase(BaseModel):
    advert_id: int
