from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pathlib import Path
from typing import List
from dishka.integrations.fastapi import FromDishka, inject
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user
from src.users.models.users import User
from src.advert.services.gallery_serv import GalleryService
from src.building.services.house import HouseService

router = APIRouter()

MEDIA_PATH = Path("media/houses")

@router.post("/houses/{house_id}/gallery", status_code=201)
@inject
async def upload_gallery_images(
    house_id: int,
    current_user: User = Depends(get_current_user),
    files: List[UploadFile] = File(...),
    session: FromDishka[AsyncSession] = Depends(),
    gallery_service: FromDishka[GalleryService] = Depends(),
    house_service: FromDishka[HouseService] = Depends(),
):

    # Проверяем, что дом существует и принадлежит текущему пользователю
    house = await house_service.get_by_id(session, house_id)
    if not house:
        raise HTTPException(status_code=404, detail="House not found")
    if house.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    # Создаем папку для дома, если еще нет
    house_dir = MEDIA_PATH / str(house_id)
    house_dir.mkdir(parents=True, exist_ok=True)

    created_images = []

    for idx, file in enumerate(files):
        if file.content_type not in {"image/jpeg", "image/png", "image/webp"}:
            raise HTTPException(status_code=400, detail=f"Unsupported image type: {file.filename}")

        filename = f"{idx}_{file.filename}"
        save_path = house_dir / filename

        # Сохраняем файл
        with save_path.open("wb") as f:
            f.write(await file.read())

        # Создаем запись в базе
        image_record = await gallery_service.create(
            session,
            {
                "image": str(save_path.relative_to(MEDIA_PATH.parent)),  # например, "media/houses/6/0_photo.jpg"
                "is_main": idx == 0,  # первое фото - главное
                "house_id": house_id,  # связь с домом
            }
        )
        created_images.append(image_record)

    return created_images
