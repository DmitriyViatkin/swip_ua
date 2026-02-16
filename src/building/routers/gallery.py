from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pathlib import Path
from typing import List
from dishka.integrations.fastapi import FromDishka, inject
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user
from src.users.models.users import User
from src.advert.services.gallery_serv import GalleryService
from src.building.services.house import HouseService
from src.advert.services.gallery_image_service import GalleryImageService

from src.advert.services.gallery_serv import GalleryService

router = APIRouter()

MEDIA_PATH = Path("media/houses")

@router.post("/houses/{house_id}/gallery", status_code=201)
@inject
async def upload_gallery_images(
    house_id: int,
    gallery_image_service: FromDishka[GalleryImageService],
    gallery_service: FromDishka[GalleryService],
    house_service: FromDishka[HouseService],
    session: FromDishka[AsyncSession],
    files: List[UploadFile] = File(...),
):
    house = await house_service.get_by_id(session, house_id)
    if not house:
        raise HTTPException(status_code=404, detail="House not found")

    # 🔥 создаём галерею, если её нет
    if not house.gallery_id:
        gallery = await gallery_service.create(session, {})
        house.gallery_id = gallery.id
        await session.flush()

    gallery = await gallery_service.get_by_id(session, house.gallery_id)
    if not gallery:
        raise HTTPException(status_code=404, detail="Gallery not found")

    house_dir = MEDIA_PATH / str(house_id)
    house_dir.mkdir(parents=True, exist_ok=True)

    created_images = []

    for idx, file in enumerate(files):
        if file.content_type not in {"image/jpeg", "image/png", "image/webp"}:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported image type: {file.filename}",
            )

        filename = f"{idx}_{file.filename}"
        save_path = house_dir / filename

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

