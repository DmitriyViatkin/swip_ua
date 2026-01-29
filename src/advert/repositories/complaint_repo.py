from typing import List, Optional
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from src.advert.models.complaint import Complaint
from src.advert.schemas.complaint.complaint_create_sch import ComplaintCreate


class ComplaintsRepository:
    def __init__(self, session: AsyncSession):
        """
        Ініціалізація з асинхронною сесією бази даних.
        """
        self.session = session

    async def create_complaint(self, user_id: int, data: ComplaintCreate) -> Optional[Complaint]:
        """
        Створює нову скаргу.
        Повертає об'єкт скарги або None, якщо виникла помилка (наприклад, дублікат).
        """
        db_complaint = Complaint(
            user_id=user_id,
            advert_id=data.advert_id,
            reason=data.reason,
            comment=data.comment
        )

        self.session.add(db_complaint)
        try:
            await self.session.commit()
            await self.session.refresh(db_complaint)
            return db_complaint
        except Exception:
            # У разі порушення UniqueConstraint або іншої помилки БД
            await self.session.rollback()
            return None

    async def get_all_complaints(self) -> List[Complaint]:
        """
        Отримує ВСІ скарги в системі.
        Використовує joinedload для миттєвого доступу до даних автора та оголошення.
        """
        query = (
            select(Complaint)
            .options(
                joinedload(Complaint.author),
                joinedload(Complaint.advert)
            )
            .order_by(Complaint.created_at.desc())
        )

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_complaints_by_advert(self, advert_id: int) -> List[Complaint]:
        """
        Отримує всі скарги на конкретне оголошення.
        """
        query = (
            select(Complaint)
            .where(Complaint.advert_id == advert_id)
            .options(joinedload(Complaint.author))
            .order_by(Complaint.created_at.desc())
        )

        result = await self.session.execute(query)
        return result.scalars().all()

    async def delete_complaint(self, complaint_id: int) -> bool:
        """
        Видаляє скаргу (наприклад, після розгляду модератором).
        """
        query = delete(Complaint).where(Complaint.id == complaint_id)
        result = await self.session.execute(query)
        try:
            await self.session.commit()
            return result.rowcount > 0
        except Exception:
            await self.session.rollback()
            return False