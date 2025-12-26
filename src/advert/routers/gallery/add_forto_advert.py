from fastapi import APIRouter, status, HTTPException, UploadFile, File
from pathlib import Path
from dishka.integrations.fastapi import FromDishka, inject
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas.gallery_sch import GalleryRead
from ...services.gallery_image_service import GalleryImageService
from ...services.advert_serv import AdvertService
from ...services.gallery_serv import GalleryService

router = APIRouter()
MEDIA_PATH = Path("media/advert")




@router.post(
    "/{advert_id}/gallery/images",
    response_model=GalleryRead,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def upload_gallery_images(
    advert_id: int,
    gallery_image_service: FromDishka[GalleryImageService],
    gallery_service: FromDishka[GalleryService],
    advert_service: FromDishka[AdvertService],
    session: FromDishka[AsyncSession],
    files: List[UploadFile] = File(...),
):
    advert = await advert_service.get_by_id(advert_id)
    if not advert:
        raise HTTPException(status_code=404, detail="Advert not found")
    if not advert.gallery_id:
        gallery = await gallery_service.create(session, {})
        advert.gallery_id = gallery.id
        await session.flush()

    gallery = await gallery_service.get_gallery_by_advert (session,advert_id)
    if not gallery:
        raise HTTPException(status_code=404, detail="Gallery not found")

    advert_dir = MEDIA_PATH / str(advert_id)
    advert_dir.mkdir(parents=True, exist_ok=True)

    created_images = []

    for idx, file in enumerate(files):
        if file.content_type not in {"image/jpeg", "image/png", "image/webp"}:
            raise HTTPException(
                status_code=400, detail=f"Unsupported image type: {file.filename}"
            )

        filename = f"{idx}_{file.filename}"
        save_path = advert_dir / filename
        with save_path.open("wb") as f:
            f.write(await file.read())

        image_data = {
            "image": str(save_path.relative_to(MEDIA_PATH.parent)),
            "position": idx,
            "is_main": idx == 0,
            "gallery_id": gallery.id,
        }

        image_record = await gallery_image_service.create(session, image_data)
        created_images.append(image_record)

    return gallery

