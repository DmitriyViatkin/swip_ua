from typing import  Optional
from src.enums import ComplaintReasonEnum
from pydantic import BaseModel

class ComplaintBase(BaseModel):
    reason: ComplaintReasonEnum
    comment: Optional[str]=None


