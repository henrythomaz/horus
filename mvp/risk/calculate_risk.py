import json
from pathlib import Path


# ============================================================
# CONFIGURAÇÃO
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MISSION_DIR = (
    BASE_DIR
    / "tests"
    / "mission_001"
)

RESULTS_DIR = (
    MISSION_DIR
    / "results"
)

INPUT_JSON = (
    RESULTS_DIR
    / "mission_result.json"
)

OUTPUT_JSON = (
    RESULTS_DIR
    / "risk_result.json"
)


# ============================================================
# PESOS DAS CLASSES
# ============================================================
#
# Estes pesos são parâmetros OPERACIONAIS do MVP.
#
# Eles não representam, por si só, risco epidemiológico
# validado. A equipe do projeto pode ajustar esses valores
# posteriormente com base na metodologia definida.
#
# Quanto maior o peso:
# maior a contribuição da detecção para o índice de risco.
#
# ============================================================

CLASS_WEIGHTS = {
    "coconut_shell": 1.0,
    "drum": 1.0,
    "other_containers": 1.0,
    "tire": 1.0,
    "water_tank": 1.0,
}


# ============================================================
# LIMITES DOS NÍVEIS
# ============================================================
#
# O score final é contínuo.
#
# Os níveis abaixo são apenas uma classificação
# operacional para o MVP.
#
# ============================================================

LOW_THRESHOLD = 1.0
MEDIUM_THRESHOLD = 3.0
HIGH_THRESHOLD = 5.0


# ============================================================
# CLASSIFICAÇÃO DO RISCO
# ============================================================

def classify_risk(score: float) -> str:
    """
    Converte o score em um nível operacional.
    """

    if score >= HIGH_THRESHOLD:
        return "HIGH"

    if score >= MEDIUM_THRESHOLD:
        return "MEDIUM"

    if score >= LOW_THRESHOLD:
        return "LOW"

    return "VERY_LOW"


# ============================================================
# CALCULA RISCO DE UMA DETECÇÃO
# ============================================================

def calculate_detection_score(
    detection: dict,
) -> float:
    """
    Calcula a contribuição de uma detecção.

    Fórmula:

        score =
            peso_da_classe × confiança

    """

    class_name = detection.get(
        "class",
        "unknown",
    )

    confidence = float(
        detection.get(
            "confidence",
            0.0,
        )
    )

    weight = CLASS_WEIGHTS.get(
        class_name,
        1.0,
    )

    return weight * confidence


# ============================================================
# CALCULA RISCO DA IMAGEM
# ============================================================

def calculate_image_risk(
    image: dict,
) -> dict:
    """
    Calcula o risco operacional de uma imagem.

    O score da imagem é a soma das contribuições
    das detecções encontradas nela.
    """

    detections = image.get(
        "detections",
        [],
    )

    score = sum(
        calculate_detection_score(
            detection
        )
        for detection in detections
    )

    level = classify_risk(
        score
    )

    return {
        "risk_score": round(
            score,
            4,
        ),
        "risk_level": level,
    }


# ============================================================
# CARREGA RESULTADO DA MISSÃO
# ============================================================

def load_mission_result() -> dict:
    """
    Lê o mission_result.json.
    """

    if not INPUT_JSON.exists():
        raise FileNotFoundError(
            "Resultado da missão não encontrado:\n"
            f"{INPUT_JSON}"
        )

    with open(
        INPUT_JSON,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


# ============================================================
# PROCESSA MISSÃO
# ============================================================

def calculate_mission_risk(
    mission_result: dict,
) -> dict:
    """
    Calcula o risco de todas as imagens da missão.
    """

    images = mission_result.get(
        "images",
        [],
    )

    processed_images = []

    total_score = 0.0
    total_detections = 0

    detections_by_class = {}

    risk_summary = {
        "VERY_LOW": 0,
        "LOW": 0,
        "MEDIUM": 0,
        "HIGH": 0,
    }

    for image in images:

        risk = calculate_image_risk(
            image
        )

        detections = image.get(
            "detections",
            [],
        )

        total_detections += len(
            detections
        )

        total_score += risk[
            "risk_score"
        ]

        risk_summary[
            risk["risk_level"]
        ] += 1

        # --------------------------------------------
        # Conta detecções por classe
        # --------------------------------------------

        for detection in detections:

            class_name = detection.get(
                "class",
                "unknown",
            )

            detections_by_class[
                class_name
            ] = (
                detections_by_class.get(
                    class_name,
                    0,
                )
                + 1
            )

        # --------------------------------------------
        # Resultado da imagem
        # --------------------------------------------

        processed_image = {
            "filename": image[
                "filename"
            ],

            "location": image[
                "location"
            ],

            "detections": detections,

            "risk_score": risk[
                "risk_score"
            ],

            "risk_level": risk[
                "risk_level"
            ],

            "annotated_image": image.get(
                "annotated_image"
            ),
        }

        processed_images.append(
            processed_image
        )

    # ========================================================
    # MAIORES RISCOS
    # ========================================================

    highest_risk_images = sorted(
        processed_images,
        key=lambda image: image[
            "risk_score"
        ],
        reverse=True,
    )

    # ========================================================
    # RESUMO
    # ========================================================

    return {
        "mission": mission_result.get(
            "mission"
        ),

        "images_processed": len(
            processed_images
        ),

        "total_detections": (
            total_detections
        ),

        "total_risk_score": round(
            total_score,
            4,
        ),

        "average_risk_score": round(
            (
                total_score
                / len(processed_images)
                if processed_images
                else 0.0
            ),
            4,
        ),

        "risk_summary": risk_summary,

        "detections_by_class": (
            detections_by_class
        ),

        "class_weights": CLASS_WEIGHTS,

        "risk_thresholds": {
            "very_low": (
                f"< {LOW_THRESHOLD}"
            ),
            "low": (
                f">= {LOW_THRESHOLD} "
                f"and < {MEDIUM_THRESHOLD}"
            ),
            "medium": (
                f">= {MEDIUM_THRESHOLD} "
                f"and < {HIGH_THRESHOLD}"
            ),
            "high": (
                f">= {HIGH_THRESHOLD}"
            ),
        },

        "highest_risk_images": (
            highest_risk_images[:10]
        ),

        "images": processed_images,
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("HORUS - CÁLCULO DE RISCO")
    print("=" * 70)

    # --------------------------------------------------------
    # Carrega missão
    # --------------------------------------------------------

    print(
        f"\nLendo:\n"
        f"{INPUT_JSON}"
    )

    mission_result = (
        load_mission_result()
    )

    # --------------------------------------------------------
    # Calcula risco
    # --------------------------------------------------------

    result = (
        calculate_mission_risk(
            mission_result
        )
    )

    # --------------------------------------------------------
    # Salva resultado
    # --------------------------------------------------------

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        OUTPUT_JSON,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            result,
            file,
            indent=2,
            ensure_ascii=False,
        )

    # --------------------------------------------------------
    # Resumo
    # --------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("RESULTADO")
    print("=" * 70)

    print(
        f"Imagens processadas: "
        f"{result['images_processed']}"
    )

    print(
        f"Total de detecções: "
        f"{result['total_detections']}"
    )

    print(
        f"Score total: "
        f"{result['total_risk_score']}"
    )

    print(
        f"Score médio: "
        f"{result['average_risk_score']}"
    )

    print("\nDetecções por classe:")

    for class_name, count in (
        result[
            "detections_by_class"
        ].items()
    ):

        print(
            f"  {class_name}: {count}"
        )

    print("\nResumo de risco:")

    for level, count in (
        result[
            "risk_summary"
        ].items()
    ):

        print(
            f"  {level}: {count}"
        )

    print(
        f"\nResultado salvo em:\n"
        f"{OUTPUT_JSON}"
    )


if __name__ == "__main__":
    main()
