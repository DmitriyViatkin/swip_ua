from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from dishka.integrations.fastapi import FromDishka, inject

from src.advert.services.complaint_serv import ComplaintsService
from src.advert.schemas.complaint.complaint_create_sch import ComplaintCreate
from src.advert.schemas.complaint.complaint_read_sch import ComplaintRead
from src.auth.dependencies import get_current_user
from src.users.models.users import User
from src.auth.dependencies import get_current_user
from src.users.models.users import User
from typing import Annotated
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter( )




@router.get(
    "/advert/{advert_id}",
    response_model=List[ComplaintRead]
)
@inject
async def get_complaints_by_advert(
    advert_id: int,
user: CurrentUser,
    service: FromDishka[ComplaintsService],
):
    return await service.get_advert_complaints(advert_id)