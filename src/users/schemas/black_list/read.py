from .base import BlackListBase


class BlackListRead(BlackListBase):
    id: int

    class Config:
        orm_mode = True