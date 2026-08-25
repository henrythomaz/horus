from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


UPLOAD_DIR = Path("storage/images")


def save_image(
    file: UploadFile,
) -> str:

    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    extension = (
        Path(file.filename)
        .suffix
    )

    filename = (
        f"{uuid4()}{extension}"
    )

    path = (
        UPLOAD_DIR /
        filename
    )


    with open(path, "wb") as buffer:
        buffer.write(
            file.file.read()
        )


    return str(path)
