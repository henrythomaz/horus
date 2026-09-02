import json
from pathlib import Path

from PIL import Image
from ultralytics import YOLO

from extract_gps import extract_gps


# ============================================================
# CONFIGURAÇÃO
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MISSION_DIR = (
    BASE_DIR
    / "tests"
    / "mission_001"
)

IMAGES_DIR = (
    MISSION_DIR
    / "images"
)

RESULTS_DIR = (
    MISSION_DIR
    / "results"
)

ANNOTATED_DIR = (
    RESULTS_DIR
    / "images"
)

RESULT_JSON_PATH = (
    RESULTS_DIR
    / "mission_result.json"
)

MODEL_PATH = Path(
    "/home/henry/projetos/horus/apps/api/models/best2.pt"
)

CONFIDENCE = 0.49


# ============================================================
# ENCONTRA IMAGENS
# ============================================================

def find_images() -> list[Path]:
    """
    Encontra todas as imagens da missão.

    Aceita:
        .jpg
        .jpeg
        .png

    A extensão não precisa estar em maiúscula.
    """

    extensions = {
        ".jpg",
        ".jpeg",
        ".png",
    }

    if not IMAGES_DIR.exists():
        raise FileNotFoundError(
            f"Pasta de imagens não encontrada:\n"
            f"{IMAGES_DIR}"
        )

    images = [
        path
        for path in IMAGES_DIR.iterdir()
        if path.is_file()
        and path.suffix.lower() in extensions
    ]

    return sorted(images)


# ============================================================
# YOLO
# ============================================================

def run_yolo(
    model: YOLO,
    image_path: Path,
):
    """
    Executa o YOLO em uma imagem.
    """

    results = model.predict(
        source=str(image_path),
        conf=CONFIDENCE,
        save=False,
        verbose=False,
    )

    return results[0]


# ============================================================
# DETECÇÕES
# ============================================================

def get_detections(
    model: YOLO,
    result,
) -> list[dict]:
    """
    Converte as detecções do YOLO para o JSON do Horus.
    """

    detections = []

    if result.boxes is None:
        return detections

    boxes = result.boxes.xyxy.cpu().tolist()
    confidences = result.boxes.conf.cpu().tolist()
    classes = result.boxes.cls.cpu().tolist()

    for box, confidence, class_id in zip(
        boxes,
        confidences,
        classes,
    ):

        class_id = int(class_id)
        confidence = float(confidence)

        detections.append(
            {
                "class_id": class_id,
                "class": model.names[class_id],
                "confidence": confidence,
                "bbox": {
                    "x1": float(box[0]),
                    "y1": float(box[1]),
                    "x2": float(box[2]),
                    "y2": float(box[3]),
                },
            }
        )

    return detections


# ============================================================
# IMAGEM ANOTADA
# ============================================================

def save_annotated_image(
    result,
    image_path: Path,
) -> Path:
    """
    Salva a imagem anotada exatamente uma vez.

    O nome original e a extensão original são preservados.
    """

    ANNOTATED_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    annotated = result.plot()

    output_path = (
        ANNOTATED_DIR
        / image_path.name
    )

    image = Image.fromarray(
        annotated[:, :, ::-1]
    )

    image.save(
        output_path
    )

    return output_path


# ============================================================
# PROCESSAMENTO
# ============================================================

def process_mission():

    print("=" * 70)
    print("HORUS - PROCESSAMENTO DA MISSÃO")
    print("=" * 70)

    # --------------------------------------------------------
    # Verificações
    # --------------------------------------------------------

    if not MISSION_DIR.exists():
        raise FileNotFoundError(
            f"Missão não encontrada:\n"
            f"{MISSION_DIR}"
        )

    if not IMAGES_DIR.exists():
        raise FileNotFoundError(
            f"Pasta de imagens não encontrada:\n"
            f"{IMAGES_DIR}"
        )

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Modelo YOLO não encontrado:\n"
            f"{MODEL_PATH}"
        )

    # --------------------------------------------------------
    # Imagens
    # --------------------------------------------------------

    images = find_images()

    print(
        f"\nImagens encontradas: "
        f"{len(images)}"
    )

    if not images:
        raise RuntimeError(
            "Nenhuma imagem encontrada."
        )

    # --------------------------------------------------------
    # Cria diretórios de saída
    # --------------------------------------------------------

    ANNOTATED_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # Modelo
    # --------------------------------------------------------

    print("\nCarregando modelo YOLO...")

    model = YOLO(
        str(MODEL_PATH)
    )

    print("Modelo carregado.")

    # --------------------------------------------------------
    # Processa imagens
    # --------------------------------------------------------

    mission_results = []

    print("\n")
    print("=" * 70)
    print("PROCESSANDO MISSÃO")
    print("=" * 70)

    for index, image_path in enumerate(
        images,
        start=1,
    ):

        print(
            f"\n[{index}/{len(images)}] "
            f"{image_path.name}"
        )

        # ----------------------------------------------------
        # GPS
        # ----------------------------------------------------

        gps = extract_gps(
            image_path
        )

        if gps is None:
            raise RuntimeError(
                "GPS não encontrado no EXIF da imagem:\n"
                f"{image_path}"
            )

        print(
            f"GPS: "
            f"{gps['latitude']}, "
            f"{gps['longitude']}, "
            f"{gps['altitude']} m"
        )

        # ----------------------------------------------------
        # YOLO
        # ----------------------------------------------------

        result = run_yolo(
            model,
            image_path,
        )

        detections = get_detections(
            model,
            result,
        )

        print(
            f"Detecções: "
            f"{len(detections)}"
        )

        # ----------------------------------------------------
        # Salva imagem anotada
        # ----------------------------------------------------

        annotated_path = (
            save_annotated_image(
                result,
                image_path,
            )
        )

        # ----------------------------------------------------
        # Resultado da imagem
        # ----------------------------------------------------

        image_result = {
            "filename": image_path.name,

            "location": {
                "latitude": gps["latitude"],
                "longitude": gps["longitude"],
                "altitude": gps["altitude"],
            },

            "detections": detections,

            "annotated_image": str(
                annotated_path.relative_to(
                    MISSION_DIR
                )
            ),
        }

        mission_results.append(
            image_result
        )

    # --------------------------------------------------------
    # JSON FINAL
    # --------------------------------------------------------

    output = {
        "mission": MISSION_DIR.name,

        "images_processed": (
            len(mission_results)
        ),

        "confidence_threshold": (
            CONFIDENCE
        ),

        "gps_source": (
            "image_exif"
        ),

        "model": str(
            MODEL_PATH
        ),

        "images": mission_results,
    }

    with open(
        RESULT_JSON_PATH,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            output,
            file,
            indent=2,
            ensure_ascii=False,
        )

    # --------------------------------------------------------
    # Resumo
    # --------------------------------------------------------

    total_detections = sum(
        len(image["detections"])
        for image in mission_results
    )

    print("\n")
    print("=" * 70)
    print("MISSÃO CONCLUÍDA")
    print("=" * 70)

    print(
        f"Imagens processadas: "
        f"{len(mission_results)}"
    )

    print(
        f"Total de detecções: "
        f"{total_detections}"
    )

    print(
        f"\nJSON:"
        f"\n{RESULT_JSON_PATH}"
    )

    print(
        f"\nImagens anotadas:"
        f"\n{ANNOTATED_DIR}"
    )


# ============================================================
# MAIN
# ============================================================

def main():
    process_mission()


if __name__ == "__main__":
    main()
