from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status, HTTPException

from src.advert.schemas.image_sch import AdvertUpdateWithImages
from ..schemas.advert.advert_read_sch import AdvertRead
from ..services.advert_serv import AdvertService

router = APIRouter()




@router.patch(
    "/advert/{advert_id}",
    response_model=AdvertRead,
    status_code=status.HTTP_200_OK,
)
@inject
async def update_advert(
    advert_id: int,
    data: AdvertUpdateWithImages,
    advert_service: FromDishka[AdvertService],
):


    try:
        advert = await advert_service.update(
            advert_id,
            data,
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Advert not found")

    return advert
