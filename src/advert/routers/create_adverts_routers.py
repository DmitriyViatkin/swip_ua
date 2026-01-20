import base64
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from dishka.integrations.fastapi import FromDishka, inject
from src.advert.schemas.image_sch import AdvertUpdateWithImages
from ..schemas.advert.advert_create_sch import AdvertCreate
from ..schemas.advert.advert_read_sch import AdvertRead
from src.advert.services.advert_serv import AdvertService
from src.advert.services.gallery_serv import GalleryService
from src.advert.services.gallery_image_service import GalleryImageService
from src.advert.schemas.image_sch import  AdvertCreateWithImages

router = APIRouter()

  # base64 изображения


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
    data: AdvertCreateWithImages,
):
    advert_data = data.dict(exclude={"images"})

    # создаём объявление
    advert = await advert_service.create(advert_data)

    # если есть изображения — создаём галерею
    if data.images:
        gallery = await gallery_service.create(session, {})
        advert.gallery_id = gallery.id
        await session.flush()

        advert_dir = Path("uploads/advert") / str(advert.id)
        advert_dir.mkdir(parents=True, exist_ok=True)

        for idx, image_obj in enumerate(data.images):
            if not image_obj.base64:
                continue

            base64_str = image_obj.base64
            header, encoded = (
                base64_str.split(",", 1)
                if "," in base64_str
                else ("data:image/png;base64", base64_str)
            )

            img_data = base64.b64decode(encoded)
            ext = "png" if "png" in header else "jpg"
            filename = f"{idx}.{ext}"
            path = advert_dir / filename

            with path.open("wb") as f:
                f.write(img_data)

            await gallery_image_service.create(
                session,
                {
                    "gallery_id": gallery.id,
                    "image": str(path.relative_to("uploads")),
                    "position": image_obj.position or idx,
                    "is_main": idx == 0,
                },
            )


    advert = await advert_service.get_by_id(advert.id)

    return advert

