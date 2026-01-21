from pydantic import BaseModel, computed_field,field_validator, ConfigDict
from config.config.settings import user_settings


class GalleryImageRead(BaseModel):
    id: int
    image: str
    position: int

    @field_validator("image", mode= "after")
    @classmethod
    def format_image_url(cls, v: str)->str:
        """Подменяет относительный путь на полный URL в поле image"""
        if v and not v.startswith(("http://", "https://")):
            return f"{user_settings.media_url}{v}"
        return v


    """@computed_field
    @property
    def url(self) -> str:
        #base_url = "https://your-domain.com/media/"
        return f'{user_settings.media_url}{self.image}'"""


    model_config = ConfigDict(from_attributes=True)