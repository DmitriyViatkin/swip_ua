from src.building.services.base import BaseService
from src.building.repositories.infrastructure import InfrastructureRepository
from src.building.models.infrastructure import Infrastructure
from sqlalchemy.ext.asyncio import AsyncSession



class InfrastructureService(BaseService[Infrastructure]):
    def __init__(self):
        super().__init__(InfrastructureRepository())

    async def update_or_create(
        self,
        session: AsyncSession,
        house_id: int,
        data: dict,
    ) -> Infrastructure:

        repo: InfrastructureRepository = self.repository

        obj = await repo.get_by_house_id(session, house_id)

        if obj is None:
            data["house_id"] = house_id
            obj = await repo.create(session, data)
        else:
            obj = await repo.update(session, obj, data)

        return obj