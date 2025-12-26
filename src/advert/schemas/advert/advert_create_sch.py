#src/advert/schemas/advert/advert_create_sch.py
from pydantic import Field
from .advert_base_sch import AdvertBase

class AdvertCreate(AdvertBase):

    build_id: int = Field(..., gt=0)



