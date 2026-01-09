from fastapi import APIRouter, status, HTTPException, UploadFile, File
from pathlib import Path
from dishka.integrations.fastapi import FromDishka, inject
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas.gallery_image_sch import   GalleryImageRead
from ...services.gallery_image_service import GalleryImageService
from ...services.advert_serv import AdvertService
from ...services.gallery_serv import GalleryService

router = APIRouter( )

@router.delete(
    "/gallery/images/{image_id}",

    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def delete_gallery_images(
        image_id: int,

        gallery_image_service: FromDishka[GalleryImageService],
        session: FromDishka[AsyncSession] ):
    image = await gallery_image_service.get_by_id(session, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    await gallery_image_service.delete(session, image)