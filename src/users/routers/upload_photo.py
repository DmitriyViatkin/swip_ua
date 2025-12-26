from fastapi import UploadFile, File
from pathlib import Path
from fastapi import APIRouter,HTTPException, Depends
from dishka.integrations.fastapi import FromDishka,inject
from fastapi.security import HTTPBearer
from src.users.schemas.user.user_read import UserRead
from src.users.models.users import User
from src.auth.dependencies import get_current_user
from src.users.services.user_service import UserService
from typing import List

MEDIA_PATH = Path("media/users")
MEDIA_PATH.mkdir(parents=True, exist_ok=True)
bearer_scheme = HTTPBearer()


router = APIRouter()

@router.post("/update-photo/{user_id}", response_model=UserRead)
@inject
async def upload_user_photo(
    user_id: int,
    current_user: User = Depends(get_current_user),
    file: UploadFile = File(...),
    user_service: FromDishka[UserService] = Depends()
):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Проверка файла
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # Генерация безопасного имени
    filename = f"user_{user_id}_{file.filename}"
    save_path = MEDIA_PATH / filename

    # Сохраняем файл
    with save_path.open("wb") as f:
        f.write(await file.read())

    # Обновляем в БД
    updated_user = await user_service.update_user_photo(user_id, filename)

    return UserRead.model_validate(updated_user, from_attributes=True)