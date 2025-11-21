# src/schemas/notification/read.py

from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, EmailStr  # Pydantic V2
# from pydantic import BaseModel, EmailStr, Field # Pydantic V1
from typing import ForwardRef, Optional, List  # <--- Добавляем ForwardRef
from .base import NotificationBase  # Предполагаемый базовый класс

# --- ForwardRef для UserRead ---
# Предполагаем, что схема UserRead находится в src/schemas/user/read.py
UserRead = ForwardRef('UserRead')


class NotificationRead(NotificationBase):
    id: int

    # Добавьте поля, которые генерируются базой данных
    date: datetime

    # --- Поля отношений ---

    # 1. Поля внешних ключей (если нужны)
    client_id: Optional[int]
    agent_id: Optional[int]

    # 2. Ссылки на связанные объекты UserRead (используем ForwardRef)
    client: Optional[UserRead]
    agent: Optional[UserRead]



    model_config = ConfigDict(
        from_attributes=True,

    )


from ..user.user_read import UserRead as URead

NotificationRead.model_rebuild(_types_namespace={'UserRead': URead})
