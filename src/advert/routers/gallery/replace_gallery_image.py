from fastapi import APIRouter, HTTPException, UploadFile, File
from pathlib import Path
from dishka.integrations.fastapi import FromDishka, inject
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas.gallery_image_sch import GalleryImageRead
from ...services.gallery_image_service import GalleryImageService
import shutil

router = APIRouter()

MEDIA_PATH = Path("media/advert")


@router.put(
    "/gallery/images_replace/{image_id}",
    response_model=GalleryImageRead,
)
@inject
async def replace_gallery_images(
    image_id: int,
    gallery_image_service: FromDishka[GalleryImageService],
    session: FromDishka[AsyncSession],
    file: UploadFile = File(...),
):
    # 1️⃣ Получаем advert_id БЕЗ lazy-load
    advert_id = await gallery_image_service.get_advert_id_by_image_id(
        session,
        image_id,
    )
    if advert_id is None:
        raise HTTPException(status_code=404, detail="Image not found")

    # 2️⃣ Получаем сам image (без relationship)
    image = await gallery_image_service.get_by_id(session, image_id)

    # 3️⃣ Папка объявления
    advert_dir = MEDIA_PATH / str(advert_id)
    advert_dir.mkdir(parents=True, exist_ok=True)

    # 4️⃣ Сохраняем файл
    save_path = advert_dir / file.filename
    with save_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 5️⃣ Относительный путь
    relative_path = str(save_path.relative_to(MEDIA_PATH.parent))

    # 6️⃣ Обновляем запись
    updated = await gallery_image_service.update(
        session,
        image.id,
        {"image": relative_path},
    )

    await session.commit()
    return updated
