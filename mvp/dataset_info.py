from pathlib import Path

DATASET = Path.home() / "projetos/horus/datasets/DATASET.yolov8"

for split in ["train", "valid", "test"]:
    images = list((DATASET / split / "images").glob("*.jpg"))
    labels = list((DATASET / split / "labels").glob("*.txt"))

    print(f"\n{split.upper()}")
    print(f"Imagens: {len(images)}")
    print(f"Labels: {len(labels)}")
