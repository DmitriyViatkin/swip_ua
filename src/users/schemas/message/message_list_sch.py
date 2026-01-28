from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LastMessage(BaseModel):
    text: str
    created_at: datetime
    is_read: bool

class Dialog(BaseModel):
    interlocutor_id: int
    last_message: LastMessage