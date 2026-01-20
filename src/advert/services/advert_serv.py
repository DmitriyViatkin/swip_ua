from src.advert.repositories.advert_repo import AdvertRepository
from src.advert.repositories.gallery_image_repo import GalleryImageRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.advert.schemas.image_sch import AdvertUpdateWithImages
from src.advert.models.advert import Advert
from src.advert.schemas.galery_order import GalleryOrder
import base64
import uuid
import os
from sqlalchemy.orm import selectinload
from sqlalchemy  import select


class AdvertService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = AdvertRepository(session)

    async def create(self, data: dict):
        advert = await self.repo.create(data)
        await self.session.commit()
        return advert

    async def get_by_id(self, advert_id: int):
        return await self.repo.get_by_id(advert_id)

    async def update(self, advert_id: int, advert_data: AdvertUpdateWithImages):
        advert = await self.repo.get_by_id(advert_id)

        if not advert:
            raise ValueError("Advert not found")

        await self.repo.update(
            advert,
            advert_data.model_dump(exclude_unset=True, exclude={"images"}),
        )

        if advert_data.images:
            await self._apply_gallery_actions(advert, advert_data.images)

        await self.session.commit()

        # 🔥 обязательно перечитываем
        return await self.get_by_id(advert_id)

    @staticmethod
    async def save_base64_image(base64_str: str, upload_dir: str = "uploads/advert/") -> str:
        # base64 строка может начинаться с "data:image/jpeg;base64,..."
        if "," in base64_str:
            header, base64_data = base64_str.split(",", 1)
        else:
            base64_data = base64_str

        # Создаем папку, если нет
        os.makedirs(upload_dir, exist_ok=True)

        # Генерируем уникальное имя файла (например, uuid + .jpg)
        filename = f"{uuid.uuid4().hex}.jpg"
        filepath = os.path.join(upload_dir, filename)

        # Декодируем base64
        image_bytes = base64.b64decode(base64_data)

        # Сохраняем файл
        with open(filepath, "wb") as f:
            f.write(image_bytes)

        # Возвращаем путь, который можно сохранить в БД (например, относительный)
        return f"advert/{filename}"

    async def _apply_gallery_actions(self, advert: Advert,  images: list,    ):
        reorder_items: list[GalleryOrder] = []

        for image_action in images:
            # delete
            if image_action.is_delete and image_action.image_id:
                obj = await self.gallery_image_repo.get_by_id_with_gallery(self.session, image_action.image_id)
                if obj:
                    await self.session.delete(obj)
                    await self.session.flush()

            # reorder (копим, применяем один раз)
            if image_action.image_id and image_action.position is not None:
                reorder_items.append(
                    GalleryOrder(
                        id=image_action.image_id,
                        position=image_action.position,
                    )
                )
                continue

            # add image
            if image_action.base64:
                image_path = await self.save_base64_image(image_action.base64)

                await self.gallery_image_repo.create(
                    self.session,
                    {
                        "gallery_id": advert.gallery.id,
                        "image": image_path,
                        "position": image_action.position,

                    },
                )

        if reorder_items:
            await self.gallery_image_repo.bulk_reorder(
                session=self.session,
                advert_id=advert.id,
                items=reorder_items,
            )

    async def get_all(self):
        return await self.repo.get_all()




