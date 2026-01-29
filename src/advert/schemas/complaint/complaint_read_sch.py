from .complaint_base_sch import ComplaintBase
from datetime import datetime
from pydantic import ConfigDict, BaseModel
from typing import List


class ComplaintRead(ComplaintBase):

    id: int
    user_id: int
    advert_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes = True)

class ComplaintList(BaseModel):

    items: List[ ComplaintRead]

    model_config = ConfigDict(from_attributes= True)
