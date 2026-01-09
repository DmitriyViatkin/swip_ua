from fastapi import APIRouter, status, HTTPException, UploadFile, File
from pathlib import Path
from dishka.integrations.fastapi import FromDishka, inject
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas.gallery_order_sch import  GalleryOrder
from ...services.gallery_image_service import GalleryImageService
from ...services.advert_serv import AdvertService
from ...services.gallery_serv import GalleryService

router = APIRouter( )


@router.put(
    "/gallery/images/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT

)
@inject
async def reorder_gallery_images(
    advert_id: int,
    items: List[GalleryOrder],
    advert_service: FromDishka[AdvertService],
    gallery_image_service: FromDishka[GalleryImageService],
    session: FromDishka[AsyncSession],
):
    advert = await advert_service.get_by_id(advert_id)
    if not advert:
        raise HTTPException(status_code=404, detail="Advert not found")

    await gallery_image_service.reorder_for_advert(
        session=session,
        advert_id=advert_id,
        items=items,
    )
