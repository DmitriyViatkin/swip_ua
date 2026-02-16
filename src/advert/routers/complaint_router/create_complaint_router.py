from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from dishka.integrations.fastapi import FromDishka, inject

from src.advert.services.complaint_serv import ComplaintsService
from src.advert.schemas.complaint.complaint_create_sch import ComplaintCreate
from src.advert.schemas.complaint.complaint_read_sch import ComplaintRead
from src.auth.dependencies import get_current_user
from src.users.models.users import User
from typing import Annotated

CurrentUser = Annotated[User, Depends(get_current_user)]


router = APIRouter(   )

@router.post(
    "/complaint/create",
    response_model=ComplaintRead,
    status_code=status.HTTP_201_CREATED
)
@inject
async def create_complaint(
    data: ComplaintCreate,
    user: CurrentUser,
    service: FromDishka[ComplaintsService],
):
    complaint = await service.report_advert(user.id, data)

    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Скарга вже існує або виникла помилка"
        )

    return complaint