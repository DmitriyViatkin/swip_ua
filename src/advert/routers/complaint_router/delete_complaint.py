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

router = APIRouter( )


@router.delete(
    "/{complaint_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def delete_complaint(
    complaint_id: int,
    service: FromDishka[ComplaintsService],
        user: CurrentUser
):
    deleted = await service.resolve_complaint(complaint_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Скаргу не знайдено"
        )
