

from config.config.settings import user_settings
from config.infra.builder import FastAPIBuilder
from src.users.router import router as users_router
from src.users.admin_routers import router as notary_router
from src.auth.router import router as auth_router
from src.building.router import router as development_router
from src.advert.router import router as adverts_router



builder = FastAPIBuilder(
    title=user_settings.TITLE,
    description=user_settings.DESCRIPTION,

)

app = builder.get_app()

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(notary_router)
app.include_router(development_router)
app.include_router(adverts_router)





