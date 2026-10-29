import uuid
from pathlib import Path
from PIL import Image, ImageOps

FOLDER = Path(__file__).parent / "uploads"
EXTENSIONS = {".jpg", ".jpeg", ".png"}
MAXSIZE = (1024, 1024)


def save_photo(upload_file):
    ext = Path(upload_file.filename).suffix.lower()
    if ext not in EXTENSIONS:
        raise ValueError("File type not accepted.")

    try:
        image = Image.open(upload_file.stream)
        image = ImageOps.exif_transpose(image)
    except Exception:
        raise ValueError("File not valid.")

    image = image.convert("RGB")
    image.thumbnail(MAXSIZE)

    FOLDER.mkdir(exist_ok=True)
    filename = f"{uuid.uuid4().hex}.jpg"
    image.save(FOLDER / filename, "JPEG", quality = 85)
    return filename


def get_path(filename):
    return FOLDER / filename