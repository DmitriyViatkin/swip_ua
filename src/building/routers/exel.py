from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from dishka.integrations.fastapi import FromDishka, inject

from src.auth.dependencies import get_current_user
from src.users.models.users import User
from src.building.services.document import DocumentService
from src.building.services.house import HouseService

router = APIRouter()


@router.post(
    "/houses/{house_id}/spreadsheets",
    status_code=status.HTTP_201_CREATED,
)
@inject
async def upload_spreadsheet( house_id: int, session: FromDishka[AsyncSession],
                              document_service: FromDishka[DocumentService],house_service: FromDishka[HouseService],
                               current_user: User = Depends(get_current_user), file: UploadFile = File(...),):
    if file.content_type not in {
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }:
        raise HTTPException(status_code=400, detail="Unsupported spreadsheet type")