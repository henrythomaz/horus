from pathlib import Path
from typing import Optional

from PIL import Image
from PIL.ExifTags import GPSTAGS


def _convert_to_degrees(value):
    """
    Converte coordenadas EXIF no formato:
    graus, minutos, segundos

    para graus decimais.
    """
    degrees = float(value[0])
    minutes = float(value[1])
    seconds = float(value[2])

    return degrees + (minutes / 60.0) + (seconds / 3600.0)


def _get_gps_value(gps_data, key):
    """
    Procura um campo GPS pelo nome.
    """
    for tag_id, value in gps_data.items():
        tag_name = GPSTAGS.get(tag_id)

        if tag_name == key:
            return value

    return None


def extract_gps(image_path: str | Path) -> Optional[dict]:
    """
    Extrai latitude, longitude e altitude dos metadados EXIF
    de uma imagem.

    Retorna None caso a imagem não possua GPS.
    """

    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(
            f"Imagem não encontrada: {image_path}"
        )

    with Image.open(image_path) as image:
        exif = image.getexif()

        if not exif:
            return None

        gps_data = exif.get_ifd(34853)

        if not gps_data:
            return None

        latitude = _get_gps_value(gps_data, "GPSLatitude")
        latitude_ref = _get_gps_value(gps_data, "GPSLatitudeRef")

        longitude = _get_gps_value(gps_data, "GPSLongitude")
        longitude_ref = _get_gps_value(gps_data, "GPSLongitudeRef")

        altitude = _get_gps_value(gps_data, "GPSAltitude")
        altitude_ref = _get_gps_value(gps_data, "GPSAltitudeRef")

        if (
            latitude is None
            or latitude_ref is None
            or longitude is None
            or longitude_ref is None
        ):
            return None

        latitude = _convert_to_degrees(latitude)
        longitude = _convert_to_degrees(longitude)

        if latitude_ref == "S":
            latitude *= -1

        if longitude_ref == "W":
            longitude *= -1

        if altitude is not None:
            altitude = float(altitude)

            # GPSAltitudeRef = 1 significa abaixo do nível do mar.
            if altitude_ref == 1:
                altitude *= -1

        return {
            "latitude": latitude,
            "longitude": longitude,
            "altitude": altitude,
        }


def main():
    import sys

    if len(sys.argv) != 2:
        print("Uso:")
        print("  python extract_gps.py caminho/da/imagem.JPG")
        return

    image_path = sys.argv[1]

    try:
        gps = extract_gps(image_path)

        print(f"Imagem: {image_path}")

        if gps is None:
            print("GPS não encontrado nos metadados da imagem.")
            return

        print(f"Latitude:  {gps['latitude']}")
        print(f"Longitude: {gps['longitude']}")
        print(f"Altitude:  {gps['altitude']}")

    except Exception as error:
        print(f"Erro: {error}")


if __name__ == "__main__":
    main()
