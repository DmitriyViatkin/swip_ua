from typing import List, Optional
from fastapi import APIRouter, HTTPException

from src.users.repositories.user_repository import UserRepository
from src.users.repositories.subscriptions_repository import SubscriptionRepository
from src.users.repositories.notification_repository import NotificationRepository
from src.users.repositories.redirection_repository import RedirectionRepository

from src.users.schemas.user.user_create import UserCreateSchema
from src.users.schemas.user.user_update import UserUpdate
from src.users.schemas.user.user_read import UserRead

from src.users.schemas.subscription.create import SubscriptionCreate
from src.users.schemas.notification.create import NotificationCreate
from src.users.schemas.redirections import RedirectionCreate
from src.auth.security.password import hash_password
from src.enums import UserRole


class UserService:
    """Business logic for User."""

    def __init__(
        self,
        user_repository: UserRepository,
        subscription_repository: SubscriptionRepository,
        notification_repository: NotificationRepository,
        redirection_repository: RedirectionRepository,
    ):
        self.user_repository = user_repository
        self.subscription_repository = subscription_repository
        self.notification_repository = notification_repository
        self.redirection_repository = redirection_repository


    async def get_user(self, user_id: int) -> Optional[UserRead]:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            return None
        return UserRead.model_validate(user)


    async def get_all_users(self, role: Optional[str] = None):
        return await self.user_repository.get_all(role)

    async def create_user(
            self,
            data: UserCreateSchema,
            role: UserRole = UserRole.CLIENT,
            agent_id: Optional[int] = None,
            subscription_data: Optional[SubscriptionCreate] = None,
            notifications_data: Optional[List[NotificationCreate]] = None,
            redirections_data: Optional[List[RedirectionCreate]] = None,
    ) -> UserRead:
        data_dict = data.model_dump()

        # Устанавливаем роль
        data_dict["role"] = role

        # Хешируем пароль
        data_dict["password"] = hash_password(data_dict["password"])

        # Привязка к агенту (если есть)
        if agent_id is not None:
            data_dict["agent_id"] = agent_id

        # Создаем пользователя
        user = await self.user_repository.create(**data_dict)

        # ───────────── Подписка ─────────────
        if subscription_data is None:
            subscription_data = SubscriptionCreate(
                user_id=user.id,
                auto_renewal=True
            )
        else:
            subscription_data.user_id = user.id

        await self.subscription_repository.create(
            **subscription_data.model_dump()
        )

        # ───────────── Уведомления ─────────────
        if not notifications_data:
            default_notification = NotificationCreate(
                client_id=None,
                agent_id=None,
                is_me=False,
                is_me_agent=False,
                is_agent=False,
                turn_off=False,
                user_id=user.id,
            )
            await self.notification_repository.create(
                **default_notification.model_dump()
            )
        else:
            for notification in notifications_data:
                notif_data = notification.model_dump()
                notif_data["user_id"] = user.id
                await self.notification_repository.create(**notif_data)

        # ───────────── Редиректы ─────────────
        if not redirections_data:
            default_redirection = RedirectionCreate(user_id=user.id)
            await self.redirection_repository.create(
                **default_redirection.model_dump()
            )
        else:
            for redirection in redirections_data:
                redir_data = redirection.model_dump()
                redir_data["user_id"] = user.id
                await self.redirection_repository.create(**redir_data)

        # Загружаем пользователя со всеми связями
        user = await self.user_repository.get_by_id(user.id)
        if not user:
            raise ValueError("User not found after creation")

        return UserRead.model_validate(user)

    async def update_user(self, user_id: int, data: UserUpdate) -> Optional[UserRead]:
        user = await self.user_repository.update(
            user_id,
            **data.model_dump(exclude_unset=True)
        )
        if not user:
            return None

        return UserRead.model_validate(user, from_attributes=True)


    async def delete_user(self, user_id: int) -> None:
        await self.user_repository.delete(user_id)


    async def get_user_by_role(self, role: UserRole) -> List[UserRead]:
        users = await self.user_repository.get_by_role(role)
        return [UserRead.model_validate(u) for u in users]

    async def update_user_photo(self, user_id: int, filename: str):
        return await self.user_repository.update_photo(user_id, filename)


    async def email_verified(self, user_id : int):

        user = await self.user_repository.verified_email(user_id)
        if not user:
            return None
        return UserRead.model_validate(user)

    async def check_user_before_code_request(self, email: str):
        user = await self.user_repository.get_by_email(email)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.is_verified:
            raise HTTPException(status_code=400, detail="Email already verified")

        return user