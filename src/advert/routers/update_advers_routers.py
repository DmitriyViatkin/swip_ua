from fastapi import APIRouter, Depends, status,HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from .gallery.replace_gallery_image import MEDIA_PATH
from ..schemas.advert.advert_update_sch import AdvertUpdate
from ..schemas.advert.advert_read_sch import AdvertRead
from ..schemas.galery_order import GalleryOrder
from ..services.advert_serv import AdvertService
from src.users.models.users import User
from dishka.integrations.fastapi import FromDishka, inject
from typing import Optional, List
from   src.advert.services.gallery_image_service import GalleryImageService
from   src.advert.services.gallery_serv import GalleryService

router = APIRouter()


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
    data: AdvertUpdate = Depends(AdvertUpdate.as_form),
    files: list[UploadFile] = File(default=[]),
    image_to_delete: Optional[list[int]] = None,
    #order: Optional[list[GalleryOrder]] = None,
):
    async with session.begin():

        # 1️бновляем объявление
        advert = await advert_service.update(
            advert_id,
            data.model_dump(exclude_unset=True),
        )

        if not advert:
            raise HTTPException(404, "Advert not found")

        # 2️даление изображений
        if image_to_delete:
            for image_id in image_to_delete:
                image = await gallery_image_service.get_with_gallery(
                    session, image_id
                )
                if not image:
                    continue

                file_path = MEDIA_PATH.parent / image.image
                if file_path.exists():
                    file_path.unlink()

                await session.delete(image)

        # 3️добавление изображений
        if files:
            advert_dir = MEDIA_PATH / str(advert.id)
            advert_dir.mkdir(parents=True, exist_ok=True)

            for file in files:
                if file.content_type not in {
                    "image/jpeg",
                    "image/png",
                    "image/webp",
                }:
                    raise HTTPException(400, "Unsupported image type")

                save_path = advert_dir / file.filename
                with save_path.open("wb") as f:
                    f.write(await file.read())

                await gallery_service.add_image_to_advert(
                    session=session,
                    advert_id=advert.id,
                    image_data={
                        "filename": str(
                            save_path.relative_to(MEDIA_PATH.parent)
                        ),
                    },
                )

        # 4️ reorder изображений
        """
        if order:
            await gallery_image_service.reorder_for_advert(
                session=session,
                advert_id=advert.id,
                items=order,
            )
        """
    await session.refresh(advert)
    return advert

