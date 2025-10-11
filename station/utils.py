import uuid
from pathlib import Path
from django.utils.text import slugify

def create_bus_image_path(bus: "Bus", filename: str) -> Path:
    path = f"{slugify(bus.info)}-{uuid.uuid4()}" + Path(filename).suffix
    return Path("uploads/buses/") / Path(path)
