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
from src.advert.routers.filters_routers.general_filter_routers import router as filter_router
from src.advert.routers.moderation.general_moderation_rout import router as moderation
from src.users.routers.message.general_message_router import  router as message


mimetypes.add_type('image/jpeg', '.jpg')
mimetypes.add_type('image/jpeg', '.jpeg')
mimetypes.add_type('image/png', '.png')


builder = FastAPIBuilder(
    title=user_settings.TITLE,
    description=user_settings.DESCRIPTION,
)
app = builder.get_app()


absolute_media_path = user_settings.MEDIA_DIR.resolve()
absolute_media_path.mkdir(parents=True, exist_ok=True)


app.mount(
    user_settings.MEDIA_PREFIX.rstrip("/"),
    StaticFiles(directory=str(absolute_media_path)),
    name="media"
)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(message)
app.include_router(notary_router)
app.include_router(development_router)
app.include_router(adverts_router)
app.include_router( filter_router)
app.include_router(moderation)