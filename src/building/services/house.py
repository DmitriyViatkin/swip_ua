from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from src.building.services.base import BaseService
from src.building.repositories.house import HouseRepository
from src.building.models.house import House
from src.users.models.users import User

class HouseService(BaseService[House]):
    def __init__(self, repository: HouseRepository):
        super().__init__(repository)

    async def upsert(
        self,
        data: dict,
        current_user: User,
        house_id: int | None = None,
        session: AsyncSession = None,  # session передаем извне
    ) -> House:
        if session is None:
            raise ValueError("Session is required")  # или логика fallback

        if house_id:
            house = await self.repository.get_by_id(session, house_id)

            if house and house.user_id != current_user.id:
                raise HTTPException(status_code=403, detail="Forbidden")

            if house:
                return await self.repository.update(session, house, data)

        return await self.repository.create(
            session,
            {
                **data,
                "user_id": current_user.id,
            },
        )