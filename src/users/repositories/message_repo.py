from typing import List
from sqlalchemy import select, or_, and_, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.users.models.message import Message
from src.users.schemas.message.message_create_sch import MessageCreate


class MessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_message(self, sender_id: int, schema: MessageCreate) -> Message:
        """Создает новое сообщение в базе."""
        new_message = Message(
            sender_id=sender_id,
            recipient_id=schema.recipient_id,
            text=schema.text
        )
        self.session.add(new_message)
        await self.session.commit()
        await self.session.refresh(new_message)
        return new_message

    async def get_chat_history(self, user_id: int, contact_id: int, limit: int = 50) -> List[Message]:
        """Возвращает историю переписки между двумя пользователями."""
        query = select(Message).where(
            or_(
                and_(Message.sender_id == user_id, Message.recipient_id == contact_id),
                and_(Message.sender_id == contact_id, Message.recipient_id == user_id)
            )
        ).order_by(Message.created_at.asc()).limit(limit)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def mark_as_read(self, message_ids: List[int], recipient_id: int):
        """Помечает сообщения как прочитанные (только если получатель — текущий юзер)."""
        query = update(Message).where(
            and_(
                Message.id.in_(message_ids),
                Message.recipient_id == recipient_id
            )
        ).values(is_read=True)

        await self.session.execute(query)
        await self.session.commit()

    async def get_unread_count(self, user_id: int) -> int:
        """Считает общее количество непрочитанных сообщений для пользователя."""
        query = select(Message).where(
            and_(Message.recipient_id == user_id, Message.is_read == False)
        )
        result = await self.session.execute(query)
        return len(result.scalars().all())