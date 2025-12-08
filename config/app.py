

from config.config.settings import user_settings
from config.infra.builder import FastAPIBuilder
from src.users.router import router as users_router
from src.users.notary_routers import router as notary_router
from src.auth.router import router as auth_router

builder = FastAPIBuilder(
    title=user_settings.TITLE,
    description=user_settings.DESCRIPTION,

)

app = builder.get_app()

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(notary_router)






