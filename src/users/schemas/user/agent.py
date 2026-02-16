from pydantic import BaseModel
from typing import Optional

class UserAgentRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone: str
    email: str


    model_config = {
            "from_attributes": True
        }