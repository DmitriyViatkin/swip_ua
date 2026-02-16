import base64
import uuid
from pathlib import Path


def save_base64_image(base64_str: str, advert_id: int) -> str:
    # если пришёл "чистый" base64
    if not base64_str.startswith("data:image"):
        base64_str = f"data:image/jpeg;base64,{base64_str}"

    header, data = base64_str.split(",", 1)

    ext = header.split("/")[1].split(";")[0]

    image_bytes = base64.b64decode(data)

    folder = Path(f"media/advert/{advert_id}")
    folder.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid.uuid4()}.{ext}"
    file_path = folder / filename

    with open(file_path, "wb") as f:
        f.write(image_bytes)

    return f"/media/advert/{advert_id}/{filename}"
