
from ultralytics import YOLO


def main():
    model = YOLO(
        "/home/henry/projetos/horus/runs/detect/runs/horus_1280_50/weights/last.pt"
    )

    model.train(
        resume=True,
        batch=2,
        workers=0
    )


if __name__ == "__main__":
    main()
