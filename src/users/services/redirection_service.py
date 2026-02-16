from typing import List, Optional
from src.users.schemas.redirections import RedirectionCreate, RedirectionRead, RedirectionUpdate
from src.users.repositories.redirection_repository import RedirectionRepository


class RedirectionService:
    """ Business logic for Redirections """

    def __init__(self, repo: RedirectionRepository):
        self.repo = repo

    async def get_redirection(self, redir_id: int) -> Optional[RedirectionRead]:
        redir = await self.repo.get_by_id(redir_id)
        if not redir:
            return None
        return RedirectionRead.model_validate(redir)

    async def get_all_redirections(self) -> List[RedirectionRead]:
        redirs = await self.repo.get_all()
        return [RedirectionRead.model_validate(r) for r in redirs]

    async def get_by_user(self, user_id: int) -> List[RedirectionRead]:
        redirs = await self.repo.get_by_user(user_id)
        return [RedirectionRead.model_validate(r) for r in redirs]

    async def create_redirection(self, data: RedirectionCreate) -> RedirectionRead:
        redir = await self.repo.create(**data.model_dump())
        return RedirectionRead.model_validate(redir)

    async def update_redirection(self, redir_id: int, data: RedirectionUpdate) -> Optional[RedirectionRead]:
        redir = await self.repo.update(redir_id, **data.model_dump(exclude_unset=True))
        if not redir:
            return None
        return RedirectionRead.model_validate(redir)

    async def delete_redirection(self, redir_id: int) -> None:
        await self.repo.delete(redir_id)
