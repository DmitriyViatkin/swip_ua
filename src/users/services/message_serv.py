from fastapi import HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.users.repositories.message_repo import MessageRepository
from src.users.schemas.message.message_create_sch import MessageCreate
from src.users.models.message import Message


class MessageService:
    def __init__(self, session: AsyncSession):
        self.repository = MessageRepository(session)

    async def send_message(self, sender, data: MessageCreate) -> Message:
        """
        Бизнес-логика отправки сообщения.
        """
        # 1. Проверка: нельзя писать самому себе
        if sender.id == data.recipient_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot send messages to yourself."
            )

        # 2. Пример логики из вашей модели User: проверка черного списка
        # Здесь мы могли бы проверить, не заблокировал ли recipient нашего sender'а
        # (Предположим, у вас в БД есть логика проверки black_list)

        # 3. Сохранение
        return await self.repository.create_message(sender_id=sender.id, schema=data)

    async def get_messages_with_user(self, user_id: int, contact_id: int) -> List[Message]:
        """
        Получение истории и автоматическая пометка сообщений как прочитанных.
        """
        messages = await self.repository.get_chat_history(user_id, contact_id)

        # Собираем ID непрочитанных сообщений, где текущий юзер — получатель
        unread_ids = [
            m.id for m in messages
            if m.recipient_id == user_id and not m.is_read
        ]

        if unread_ids:
            await self.repository.mark_as_read(unread_ids, user_id)

        return messages

    async def get_my_unread_count(self, user_id: int) -> int:
        """Прослойка для получения счетчика."""
        return await self.repository.get_unread_count(user_id)