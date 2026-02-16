from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.advert.repositories.complaint_repo import ComplaintsRepository
from src.advert.schemas.complaint.complaint_create_sch import ComplaintCreate
from src.advert.models.complaint import Complaint


class ComplaintsService:
    def __init__(self, session: AsyncSession):
        self.repository = ComplaintsRepository(session)

    async def report_advert(self, user_id: int, data: ComplaintCreate) -> Optional[Complaint]:
        """
        Логіка подання скарги користувачем.
        Тут можна додати перевірку: чи не скаржиться автор на власне оголошення.
        """
        # Можна додати бізнес-логіку, наприклад:
        # if await self.is_user_owner(user_id, data.advert_id):
        #     raise Exception("Ви не можете скаржитися на власне оголошення")

        complaint = await self.repository.create_complaint(user_id, data)


        if complaint:
            print(f"Нова скарга на оголошення {data.advert_id} від користувача {user_id}")

        return complaint

    async def get_all_for_moderation(self) -> List[Complaint]:
        """
        Отримання списку скарг для модераторів.
        """
        return await self.repository.get_all_complaints()

    async def get_advert_complaints(self, advert_id: int) -> List[Complaint]:
        """
        Отримання всіх скарг на конкретне оголошення.
        """
        return await self.repository.get_complaints_by_advert(advert_id)

    async def resolve_complaint(self, complaint_id: int):
        """
        Видалення або закриття скарги після перевірки.
        """
        return await self.repository.delete_complaint(complaint_id)