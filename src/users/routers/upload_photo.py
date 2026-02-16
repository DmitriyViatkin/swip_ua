import aiofiles
from fastapi import UploadFile, File, APIRouter, HTTPException, Depends
from pathlib import Path
from dishka.integrations.fastapi import FromDishka, inject
from src.users.schemas.user.user_read import UserRead
from src.users.models.users import User
from src.users.services.user_service import UserService
from src.auth.role_dependencies import require_roles
from src.enums import UserRole

MEDIA_PATH = Path("media/users")
MEDIA_PATH.mkdir(parents=True, exist_ok=True)

router = APIRouter()

@router.post("/update-photo/{user_id}", response_model=UserRead)
@inject
async def upload_user_photo(
    user_id: int,
    user_service: FromDishka[UserService],
    current_user: User = Depends(require_roles(UserRole.CLIENT, UserRole.ADMIN)),
    file: UploadFile = File(...),

):
    # Проверка прав
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Проверка типа файла
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # Генерация безопасного имени
    filename = f"user_{user_id}_{file.filename}"
    save_path = MEDIA_PATH / filename

    # Асинхронное сохранение файла
    async with aiofiles.open(save_path, "wb") as f:
        await f.write(await file.read())

    # Обновление в БД
    updated_user = await user_service.update_user_photo(user_id, filename)

    return UserRead.model_validate(updated_user, from_attributes=True)
