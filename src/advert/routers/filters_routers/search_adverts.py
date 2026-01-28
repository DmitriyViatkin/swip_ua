from fastapi import APIRouter, status, HTTPException, Depends,  Query
from dishka.integrations.fastapi import FromDishka, inject
from src.auth.dependencies import get_current_user
from src.users.models.users import User
from src.advert.services.filter_serv import FilterService
from src.advert.schemas.filters.filters_create_sch import FilterCreate

router = APIRouter(   )


@router.get("/search")
@inject
async def search_adverts(
    service: FromDishka[FilterService],
    rooms: int | None = Query(None),
    price_from: float | None = Query(None),
    price_to: float | None = Query(None),
    area_from: float | None = Query(None),
    area_to: float | None = Query(None),

    type_build: str | None = Query(None),
    utility_bills: str | None = Query(None),
    distance_to_the_sea: int | None = Query(None),
    ceiling_height: float | None = Query(None),




):
    """
    Поиск объявлений без сохранения фильтра
    """

    filter_data = FilterCreate(
        rooms=rooms,
        price_from=price_from,
        price_to=price_to,
        area_from=area_from,
        area_to=area_to,
        type_build=type_build,
        utility_bills=utility_bills,
        distance_to_the_sea=distance_to_the_sea,
        ceiling_height=ceiling_height,

    )

    results = await service.search(filter_data)

    return {
        "count": len(results),
        "results": results
    }