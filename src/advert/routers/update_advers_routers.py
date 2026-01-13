import json
import base64
from pathlib import Path
from fastapi import APIRouter, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from ..schemas.advert.advert_update_sch import AdvertUpdate
from ..schemas.advert.advert_read_sch import AdvertRead
from ..schemas.galery_order import GalleryOrder
from ..services.advert_serv import AdvertService
from src.advert.services.gallery_image_service import GalleryImageService
from src.advert.services.gallery_serv import GalleryService
from dishka.integrations.fastapi import FromDishka, inject
from .gallery.replace_gallery_image import MEDIA_PATH

router = APIRouter()


class AdvertUpdateWithImages(AdvertUpdate):
    images: Optional[List[str]] = None
    order: Optional[List[GalleryOrder]] = None
    image_to_delete: Optional[List[int]] = None


@router.patch(
    "/advert/{advert_id}",
    response_model=AdvertRead,
    status_code=status.HTTP_200_OK,
)
@inject
async def update_advert(
    advert_id: int,
    session: FromDishka[AsyncSession],
    advert_service: FromDishka[AdvertService],
    gallery_image_service: FromDishka[GalleryImageService],
    gallery_service: FromDishka[GalleryService],
    data: AdvertUpdateWithImages,
):
    async with session.begin():
        # 1️ обновляем advert → получаем ID
        advert_id = await advert_service.update(
            advert_id,
            data.model_dump(exclude_unset=True, exclude={"images", "order", "image_to_delete"}),
        )

        if not advert_id:
            raise HTTPException(404, "Advert not found")

        # 2 удаление изображений
        if data.image_to_delete:
            for image_id in data.image_to_delete:
                image = await gallery_image_service.get_with_gallery(session, image_id)
                if not image:
                    continue

                file_path = MEDIA_PATH.parent / image.image
                if file_path.exists():
                    file_path.unlink()

                await session.delete(image)


            await session.flush()


            await gallery_image_service.reorder_for_advert(
                session=session,
                advert_id=advert_id,
                items=[],
            )
        # 3️добавление изображений (base64)
        if data.images:
            advert_dir = MEDIA_PATH / str(advert_id)
            advert_dir.mkdir(parents=True, exist_ok=True)

            for idx, img_base64 in enumerate(data.images):
                try:
                    header, encoded = img_base64.split(",", 1)
                    img_data = base64.b64decode(encoded)
                except Exception:
                    raise HTTPException(400, f"Invalid base64 image at index {idx}")

                ext = header.split("/")[1].split(";")[0]  # png, jpg, webp
                if ext not in {"png", "jpeg", "jpg", "webp"}:
                    raise HTTPException(400, f"Unsupported image type: {ext}")

                filename = f"{idx}.{ext}"
                save_path = advert_dir / filename
                with save_path.open("wb") as f:
                    f.write(img_data)

                await gallery_service.add_image_to_advert(
                    session=session,
                    advert_id=advert_id,
                    image_data={
                        "filename": str(save_path.relative_to(MEDIA_PATH.parent)),
                    },
                )

        # 4️ перестановка изображений
        if data.order:
            await gallery_image_service.reorder_for_advert(
                session=session,
                advert_id=advert_id,
                items=data.order,
            )

    advert = await advert_service.get_by_id(advert_id)
    return advert
