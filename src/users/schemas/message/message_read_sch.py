from .message_base_sch import MessageBase
from datetime import datetime

class MessageRead(MessageBase):
    id: int
    sender_id: int
    recipient_id: int
    created_at: datetime
    is_read: bool

    class Config:

        from_attributes = True