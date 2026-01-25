import mimetypes
from fastapi.staticfiles import StaticFiles
from config.config.settings import user_settings
from config.infra.builder import FastAPIBuilder

# Импорты роутеров
from src.users.router import router as users_router
from src.users.admin_routers import router as notary_router
from src.auth.router import router as auth_router
from src.building.router import router as development_router
from src.advert.router import router as adverts_router
from src.advert.routers.moderation.general_moderation_rout import router as moderation

# 1. Регистрация MIME-типов ПЕРЕД запуском приложения
# Это гарантирует, что браузер поймет, что файл — это картинка
mimetypes.add_type('image/jpeg', '.jpg')
mimetypes.add_type('image/jpeg', '.jpeg')
mimetypes.add_type('image/png', '.png')

# 2. Инициализация приложения
builder = FastAPIBuilder(
    title=user_settings.TITLE,
    description=user_settings.DESCRIPTION,
)
app = builder.get_app()

# 3. Настройка путей для медиа
# Используем .resolve() для получения абсолютного пути
absolute_media_path = user_settings.MEDIA_DIR.resolve()
absolute_media_path.mkdir(parents=True, exist_ok=True)

print(f"DEBUG: Static files are served from: {absolute_media_path}")

# 4. Монтируем статику ОДИН раз
# Важно: монтируем ПЕРЕД роутерами или убеждаемся, что нет конфликтов путей
app.mount(
    user_settings.MEDIA_PREFIX.rstrip("/"),  # Результат: "/media"
    StaticFiles(directory=str(absolute_media_path)),
    name="media"
)

# 5. Подключение роутеров
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(notary_router)
app.include_router(development_router)
app.include_router(adverts_router)
app.include_router(moderation)