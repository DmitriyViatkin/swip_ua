from fastapi.staticfiles import StaticFiles
from pathlib import Path

# Определяем корень проекта относительно этого файла
BASE_DIR = Path(__file__).resolve().parent

# Если папка media лежит в корне проекта:
media_path = BASE_DIR / "media"


import base64
from fastapi.responses import StreamingResponse
from io import BytesIO

@app.get("/image/{image_id}")
async def get_image(image_id: int):
    image_base64 = get_image_from_db(image_id)

    image_bytes = base64.b64decode(image_base64)

    return StreamingResponse(
        BytesIO(image_bytes),
        media_type="image/jpeg"
    )