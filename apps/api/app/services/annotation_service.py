from pathlib import Path

import cv2


OUTPUT_DIR = Path(
    "storage/processed"
)


def create_annotated_image(
    image_path: str,
    results,
) -> str:
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    image = cv2.imread(
        image_path
    )

    if image is None:
        raise FileNotFoundError(
            f"Could not read image: {image_path}"
        )

    for result in results:
        for box in result.boxes:
            coordinates = (
                box.xyxy[0]
                .cpu()
                .numpy()
                .astype(int)
            )

            x1, y1, x2, y2 = coordinates

            cv2.rectangle(
                image,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2,
            )

            class_index = int(
                box.cls[0]
            )

            confidence = float(
                box.conf[0]
            )

            label = (
                f"{class_index}: "
                f"{confidence:.2f}"
            )

            cv2.putText(
                image,
                label,
                (x1, max(y1 - 10, 0)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

    output = (
        OUTPUT_DIR
        / Path(image_path).name
    )

    success = cv2.imwrite(
        str(output),
        image,
    )

    if not success:
        raise RuntimeError(
            f"Could not write annotated image: {output}"
        )

    return str(output)
