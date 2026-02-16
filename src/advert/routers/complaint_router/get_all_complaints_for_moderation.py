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

router = APIRouter(   )

@router.get(
    "/moderation",
    response_model=List[ComplaintRead]
)
@inject
async def get_all_complaints_for_moderation(user: CurrentUser,
    service: FromDishka[ComplaintsService],
):
    return await service.get_all_for_moderation()


