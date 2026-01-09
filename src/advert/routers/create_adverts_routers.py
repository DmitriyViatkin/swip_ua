
from fastapi import APIRouter, Depends, status, UploadFile, File,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .gallery.replace_gallery_image import MEDIA_PATH
from ..schemas.advert.advert_create_sch import AdvertCreate
from ..schemas.advert.advert_update_sch import AdvertUpdate
from ..schemas.advert.advert_read_sch import AdvertRead
from src.users.models.users import User
from dishka.integrations.fastapi import FromDishka, inject
from typing import Optional, List
from src.advert.schemas.gallery_image_sch import   GalleryImageRead
from   src.advert.services.gallery_image_service import GalleryImageService
from src.advert.services.advert_serv import AdvertService
from src.advert.services.gallery_serv import GalleryService

router = APIRouter()
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
    data: AdvertCreate = Depends(AdvertCreate.as_form),
    files: List[UploadFile] = File(default=[]),

):
    # 1. Создаём объявление
    advert_data = data.dict()
    advert = await advert_service.create(advert_data)


    # 2. Если есть файлы — создаём галерею
    if files:
        gallery = await gallery_service.create(session, {})

        advert.gallery_id = gallery.id
        await session.flush()

        advert_dir = MEDIA_PATH / str(advert.id)
        advert_dir.mkdir(parents=True, exist_ok=True)

        for idx, file in enumerate(files):
            if file.content_type not in {
                "image/jpeg",
                "image/png",
                "image/webp",
            }:
                raise HTTPException(
                    status_code=400,
                    detail=f"Неподдерживаемый тип изображения: {file.filename}",
                )

            filename = f"{idx}_{file.filename}"
            save_path = advert_dir / filename

            with save_path.open("wb") as f:
                f.write(await file.read())

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


