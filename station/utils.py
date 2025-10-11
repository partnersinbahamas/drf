from pathlib import Path
from django.utils.text import slugify

def create_bus_image_path(bus: "Bus", filename: str) -> Path:
    path = f"{slugify(bus.info)}" + Path(filename).suffix
    return Path("uploads/buses/") / Path(path)
