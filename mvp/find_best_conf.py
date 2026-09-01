from pathlib import Path
from collections import defaultdict

from PIL import Image
from ultralytics import YOLO


# ============================================================
# CONFIGURAÇÃO
# ============================================================

MODEL_PATH = Path(
    "/home/henry/projetos/horus/runs/detect/runs/"
    "horus_11m_640_50/weights/best.pt"
)

DATASET = Path(
    "/home/henry/projetos/horus/datasets/DATASET.yolov8"
)

IOU_THRESHOLD = 0.50

# Faixa de confiança que será testada
CONF_VALUES = [i / 100 for i in range(1, 91)]

# Critério opcional:
# procura também o melhor F1 entre os pontos com recall >= este valor.
MIN_RECALL = 0.80


# ============================================================
# IOU
# ============================================================

def box_iou(box1, box2):
    """
    Calcula IoU entre duas caixas no formato:
    [x1, y1, x2, y2]
    """

    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])

    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    inter_w = max(0.0, x2 - x1)
    inter_h = max(0.0, y2 - y1)

    inter_area = inter_w * inter_h

    area1 = max(0.0, box1[2] - box1[0]) * max(
        0.0, box1[3] - box1[1]
    )

    area2 = max(0.0, box2[2] - box2[0]) * max(
        0.0, box2[3] - box2[1]
    )

    union = area1 + area2 - inter_area

    if union <= 0:
        return 0.0

    return inter_area / union


# ============================================================
# LEITURA DAS ANOTAÇÕES YOLO
# ============================================================

def load_labels(label_path, image_width, image_height):
    """
    Lê um arquivo YOLO:

    class_id x_center y_center width height

    e converte para:
    class_id, [x1, y1, x2, y2]
    """

    ground_truths = []

    if not label_path.exists():
        return ground_truths

    with open(label_path, "r") as file:
        for line in file:
            parts = line.strip().split()

            if len(parts) != 5:
                continue

            class_id = int(parts[0])

            x_center = float(parts[1]) * image_width
            y_center = float(parts[2]) * image_height

            width = float(parts[3]) * image_width
            height = float(parts[4]) * image_height

            x1 = x_center - width / 2
            y1 = y_center - height / 2
            x2 = x_center + width / 2
            y2 = y_center + height / 2

            ground_truths.append(
                {
                    "class_id": class_id,
                    "box": [x1, y1, x2, y2],
                }
            )

    return ground_truths


# ============================================================
# CARREGA AS PREVISÕES UMA ÚNICA VEZ
# ============================================================

def collect_predictions(model, split):
    """
    Executa o modelo uma única vez usando conf=0.01.

    Depois podemos testar vários thresholds sem
    executar novamente a rede.
    """

    image_dir = DATASET / split / "images"
    label_dir = DATASET / split / "labels"

    image_paths = sorted(
        list(image_dir.glob("*.jpg"))
        + list(image_dir.glob("*.jpeg"))
        + list(image_dir.glob("*.png"))
    )

    all_data = []

    print(f"\nColetando previsões do conjunto '{split}'...")
    print(f"Imagens: {len(image_paths)}")

    for index, image_path in enumerate(image_paths, start=1):

        with Image.open(image_path) as image:
            width, height = image.size

        label_path = label_dir / f"{image_path.stem}.txt"

        ground_truths = load_labels(
            label_path,
            width,
            height,
        )

        results = model.predict(
            source=str(image_path),
            conf=0.01,
            iou=0.70,
            imgsz=640,
            device=0,
            verbose=False,
            save=False,
        )

        predictions = []

        for result in results:

            if result.boxes is None:
                continue

            boxes = result.boxes.xyxy.cpu().tolist()
            confidences = result.boxes.conf.cpu().tolist()
            classes = result.boxes.cls.cpu().tolist()

            for box, confidence, class_id in zip(
                boxes,
                confidences,
                classes,
            ):
                predictions.append(
                    {
                        "class_id": int(class_id),
                        "confidence": float(confidence),
                        "box": box,
                    }
                )

        all_data.append(
            {
                "image": str(image_path),
                "ground_truths": ground_truths,
                "predictions": predictions,
            }
        )

        if index % 25 == 0 or index == len(image_paths):
            print(f"Processadas: {index}/{len(image_paths)}")

    return all_data


# ============================================================
# AVALIA UM CONF
# ============================================================

def evaluate_conf(all_data, conf):
    """
    Para cada imagem:

    1. remove previsões abaixo do conf;
    2. ordena por confiança;
    3. tenta casar cada previsão com uma anotação real;
    4. exige mesma classe e IoU >= IOU_THRESHOLD.

    Retorna TP, FP, FN, precision, recall e F1.
    """

    total_tp = 0
    total_fp = 0
    total_fn = 0

    for data in all_data:

        ground_truths = data["ground_truths"]

        predictions = [
            prediction
            for prediction in data["predictions"]
            if prediction["confidence"] >= conf
        ]

        predictions.sort(
            key=lambda x: x["confidence"],
            reverse=True,
        )

        matched_gt = set()

        for prediction in predictions:

            best_iou = 0.0
            best_gt_index = None

            for gt_index, gt in enumerate(ground_truths):

                if gt_index in matched_gt:
                    continue

                if gt["class_id"] != prediction["class_id"]:
                    continue

                iou = box_iou(
                    prediction["box"],
                    gt["box"],
                )

                if iou > best_iou:
                    best_iou = iou
                    best_gt_index = gt_index

            if (
                best_gt_index is not None
                and best_iou >= IOU_THRESHOLD
            ):
                total_tp += 1
                matched_gt.add(best_gt_index)
            else:
                total_fp += 1

        total_fn += len(ground_truths) - len(matched_gt)

    precision = (
        total_tp / (total_tp + total_fp)
        if (total_tp + total_fp) > 0
        else 0.0
    )

    recall = (
        total_tp / (total_tp + total_fn)
        if (total_tp + total_fn) > 0
        else 0.0
    )

    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )

    return {
        "conf": conf,
        "tp": total_tp,
        "fp": total_fp,
        "fn": total_fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


# ============================================================
# SALVA CSV
# ============================================================

def save_results(results, path):
    with open(path, "w") as file:

        file.write(
            "conf,tp,fp,fn,precision,recall,f1\n"
        )

        for result in results:
            file.write(
                f"{result['conf']:.2f},"
                f"{result['tp']},"
                f"{result['fp']},"
                f"{result['fn']},"
                f"{result['precision']:.6f},"
                f"{result['recall']:.6f},"
                f"{result['f1']:.6f}\n"
            )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("BUSCA AUTOMÁTICA DO MELHOR CONFIDENCE")
    print("=" * 70)

    print(f"\nModelo:")
    print(MODEL_PATH)

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Modelo não encontrado: {MODEL_PATH}"
        )

    model = YOLO(str(MODEL_PATH))

    # --------------------------------------------------------
    # 1. VALID
    # --------------------------------------------------------

    valid_data = collect_predictions(
        model,
        "valid",
    )

    valid_results = []

    print("\n")
    print("=" * 70)
    print("RESULTADOS NO VALID")
    print("=" * 70)

    print(
        f"{'conf':>6} "
        f"{'precision':>11} "
        f"{'recall':>11} "
        f"{'F1':>11} "
        f"{'TP':>7} "
        f"{'FP':>7} "
        f"{'FN':>7}"
    )

    for conf in CONF_VALUES:

        result = evaluate_conf(
            valid_data,
            conf,
        )

        valid_results.append(result)

        print(
            f"{result['conf']:>6.2f} "
            f"{result['precision']:>11.4f} "
            f"{result['recall']:>11.4f} "
            f"{result['f1']:>11.4f} "
            f"{result['tp']:>7} "
            f"{result['fp']:>7} "
            f"{result['fn']:>7}"
        )

    # Melhor F1 geral
    best_f1 = max(
        valid_results,
        key=lambda x: x["f1"],
    )

    # Melhor F1 mantendo recall mínimo
    recall_candidates = [
        result
        for result in valid_results
        if result["recall"] >= MIN_RECALL
    ]

    best_recall_constraint = (
        max(
            recall_candidates,
            key=lambda x: x["f1"],
        )
        if recall_candidates
        else None
    )

    print("\n")
    print("=" * 70)
    print("MELHOR CONF NO VALID")
    print("=" * 70)

    print(
        f"Melhor F1:"
        f" conf={best_f1['conf']:.2f} | "
        f"Precision={best_f1['precision']:.4f} | "
        f"Recall={best_f1['recall']:.4f} | "
        f"F1={best_f1['f1']:.4f}"
    )

    if best_recall_constraint:
        print(
            f"\nMelhor F1 com Recall >= {MIN_RECALL:.2f}:"
            f" conf={best_recall_constraint['conf']:.2f} | "
            f"Precision={best_recall_constraint['precision']:.4f} | "
            f"Recall={best_recall_constraint['recall']:.4f} | "
            f"F1={best_recall_constraint['f1']:.4f}"
        )

    valid_output = Path(
        f"best_conf_valid.csv"
    )

    save_results(
        valid_results,
        valid_output,
    )

    # --------------------------------------------------------
    # 2. TEST
    # --------------------------------------------------------

    selected_conf = best_f1["conf"]

    print("\n")
    print("=" * 70)
    print("AVALIAÇÃO FINAL NO TEST")
    print("=" * 70)

    print(
        f"Confidence escolhido pelo VALID: "
        f"{selected_conf:.2f}"
    )

    test_data = collect_predictions(
        model,
        "test",
    )

    test_result = evaluate_conf(
        test_data,
        selected_conf,
    )

    print("\nResultado no TEST:")
    print(f"Precision: {test_result['precision']:.4f}")
    print(f"Recall:    {test_result['recall']:.4f}")
    print(f"F1:        {test_result['f1']:.4f}")
    print(f"TP:        {test_result['tp']}")
    print(f"FP:        {test_result['fp']}")
    print(f"FN:        {test_result['fn']}")

    print("\n")
    print("=" * 70)
    print("RECOMENDAÇÃO")
    print("=" * 70)

    print(
        f"Use inicialmente conf={selected_conf:.2f}"
    )

    print(
        "\nOs resultados completos do VALID foram salvos em:"
    )
    print(valid_output)


if __name__ == "__main__":
    main()
