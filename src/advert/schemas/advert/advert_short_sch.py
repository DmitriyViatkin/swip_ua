#src/advert/schemas/advert/advert_short_sch.py


from pydantic import BaseModel
from decimal import Decimal

class AdvertShort(BaseModel):
    id: int
    address: str
    price: Decimal
    rooms: int

    model_config = {"from_attributes": True}