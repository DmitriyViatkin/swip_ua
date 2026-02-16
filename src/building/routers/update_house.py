from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.building.schemas.house import HouseUpsert, HouseRead
from src.building.services.house import HouseService
from src.users.models.users import User
from dishka.integrations.fastapi import FromDishka, inject
from src.auth.role_dependencies import require_roles
from src.auth.dependencies import get_current_user
from  src.enums import UserRole
from src.advert.repositories.gallery_image_repo import save_gallery_with_images
from src.advert.services.gallery_serv import GalleryService
from src.advert.services.gallery_image_service import GalleryImageService

router = APIRouter()

@router.put("/houses/{house_id}", response_model=HouseRead, status_code=status.HTTP_200_OK)
@inject
async def update_house(
    house_id: int,
    data: HouseUpsert,
    session: FromDishka[AsyncSession],
    house_service: FromDishka[HouseService],
    gallery_service: FromDishka[GalleryService],
    gallery_image_service: FromDishka[GalleryImageService],
    current_user: User = Depends(require_roles(UserRole.DEV)),
):
    # Получаем дом
    house = await house_service.get_by_id(session=session, pk=house_id)
    if not house:
        raise HTTPException(status_code=404, detail="House not found")
    if house.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Обновляем поля дома
    await house_service.update(session, house_id, data.dict(exclude={"images"}))

    # Если есть картинки — создаём/обновляем галерею
    if getattr(data, "images", None):
        try:
            # Проверяем, есть ли уже галерея у дома
            gallery_id = house.gallery_id
            gallery = await save_gallery_with_images(
                session=session,
                owner_id=house.id,
                owner_type="house",
                images=data.images,
                gallery_service=gallery_service,
                gallery_image_service=gallery_image_service,
                gallery_id=gallery_id  # передаём существующую галерею
            )

            # Если раньше не было галереи, сохраняем id
            if gallery and not house.gallery_id:
                house.gallery_id = gallery.id
                session.add(house)

        except Exception as e:
            print("Ошибка при сохранении картинок:", e)

    # Коммитим изменения
    await session.commit()

    # 🔄 Рефреш — перечитываем дом с selectinload
    house = await house_service.get_by_id(session=session, pk=house.id)

    return house
