import base64
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from dishka.integrations.fastapi import FromDishka, inject

from ..schemas.advert.advert_create_sch import AdvertCreate
from ..schemas.advert.advert_read_sch import AdvertRead
from .gallery.replace_gallery_image import MEDIA_PATH
from src.advert.services.advert_serv import AdvertService
from src.advert.services.gallery_serv import GalleryService
from src.advert.services.gallery_image_service import GalleryImageService

router = APIRouter()


class AdvertCreateWithImages(AdvertCreate):
    images: Optional[List[str]] = None  # base64 изображения


@router.post(
    "/advert",
    response_model=AdvertRead,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_advert(
    session: FromDishka[AsyncSession],
    advert_service: FromDishka[AdvertService],
    gallery_service: FromDishka[GalleryService],
    gallery_image_service: FromDishka[GalleryImageService],
    data: AdvertCreateWithImages
):
    # 1️⃣ Создаём объявление
    advert_data = data.dict(exclude={"images"})
    advert = await advert_service.create(advert_data)

    # 2️⃣ Если есть изображения
    if data.images:
        gallery = await gallery_service.create(session, {})
        advert.gallery_id = gallery.id
        await session.flush()

        advert_dir = MEDIA_PATH / str(advert.id)
        advert_dir.mkdir(parents=True, exist_ok=True)

        for idx, img_base64 in enumerate(data.images):
            # Проверка формата
            try:
                if "," in img_base64:
                    header, encoded = img_base64.split(",", 1)
                else:
                    header, encoded = "data:image/png;base64", img_base64
            except Exception:
                raise HTTPException(status_code=400, detail="Некорректный base64 формат изображения")

            # Декодирование base64
            try:
                img_data = base64.b64decode(encoded)
            except Exception:
                raise HTTPException(status_code=400, detail="Ошибка декодирования base64 изображения")

            # Определяем расширение
            ext = "png" if "png" in header else "jpg"
            filename = f"{idx}.{ext}"
            save_path = advert_dir / filename

            with save_path.open("wb") as f:
                f.write(img_data)

            await gallery_image_service.create(
                session,
                {
                    "image": str(save_path.relative_to(MEDIA_PATH.parent)),
                    "position": idx,
                    "is_main": idx == 0,
                    "gallery_id": gallery.id,
                },
            )

    return advert
