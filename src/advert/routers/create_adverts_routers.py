import base64
import binascii
import uuid
from pathlib import Path
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from dishka.integrations.fastapi import FromDishka, inject
from src.auth.dependencies import get_current_user
from src.users.models.users import User
from typing import Annotated

from src.advert.schemas.image_sch import AdvertCreateWithImages
from src.advert.schemas.advert.advert_read_sch import AdvertRead
from src.advert.services.advert_serv import AdvertService
from src.advert.services.gallery_serv import GalleryService
from src.advert.services.gallery_image_service import GalleryImageService
CurrentUser = Annotated[User, Depends(get_current_user)]
router = APIRouter()


@router.post("/advert", response_model=AdvertRead, status_code=status.HTTP_201_CREATED)
@inject
async def create_advert(
    session: FromDishka[AsyncSession],
    advert_service: FromDishka[AdvertService],
    gallery_service: FromDishka[GalleryService],
    gallery_image_service: FromDishka[GalleryImageService],
    data: AdvertCreateWithImages,
    user:CurrentUser,
):
    # 1️⃣ Создаем объявление
    advert = await advert_service.create(data.dict(exclude={"images"}))

    if data.images:
        # 2️⃣ Галерея
        gallery = await gallery_service.create(session, {})
        advert.gallery_id = gallery.id
        session.add(advert)
        await session.flush()

        # 3️⃣ Папка
        base_dir = Path("media") / "advert" / str(advert.id)
        base_dir.mkdir(parents=True, exist_ok=True)

        for idx, image in enumerate(data.images):
            if not image.base64:
                continue

            raw = image.base64.strip()

            # 4️⃣ Определяем формат
            if raw.startswith("data:image/"):
                header, raw = raw.split(",", 1)
                ext = header.split("/")[1].split(";")[0]
            else:
                ext = "jpg"  # fallback

            # 5️⃣ Декодирование
            try:
                image_bytes = base64.b64decode(raw, validate=True)
            except binascii.Error:
                raise HTTPException(400, "Invalid base64 image")

            # 6️⃣ Сохраняем
            filename = f"{uuid.uuid4()}.{ext}"
            filepath = base_dir / filename

            with open(filepath, "wb") as f:
                f.write(image_bytes)

            # 7️⃣ В БД
            await gallery_image_service.create(
                session,
                {
                    "gallery_id": gallery.id,
                    "image": f"advert/{advert.id}/{filename}",
                    "position": image.position or idx,
                },
            )

    await session.commit()
    return await advert_service.get_by_id(advert.id)
