from fastapi import APIRouter, status, HTTPException, UploadFile, File
from pathlib import Path
from dishka.integrations.fastapi import FromDishka, inject
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas.gallery_image_sch import   GalleryImageRead
from ...services.gallery_image_service import GalleryImageService
from ...services.advert_serv import AdvertService
from ...services.gallery_serv import GalleryService

router = APIRouter()





@router.get(
    "/{advert_id}/gallery/images",
    response_model=List[GalleryImageRead],
    status_code=status.HTTP_200_OK,
)
@inject
async def get_gallery_images(
        advert_id: int,
        advert_service: FromDishka[AdvertService],
        gallery_image_service: FromDishka[GalleryImageService],
        session: FromDishka[AsyncSession]
):
    advert = await  advert_service.get_by_id(advert_id)
    if not advert:
        raise HTTPException(status_code=404, detail="Advert not found")
    if not advert.gallery_id:
        return[]
    images = await gallery_image_service.get_by_gallery_id(
        session, advert.gallery_id
    )
    return images
