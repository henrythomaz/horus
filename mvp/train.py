from ultralytics import YOLO


def main():
    model = YOLO("yolo11l.pt")

    model.train(
        data="/home/henry/projetos/horus/datasets/DATASET.yolov8/data.yaml",
        epochs=50,
        imgsz=1280,
        batch=4,
        device=0,
        workers=0,
        project="runs",
        name="horus_1280_50"
    )

if __name__ == "__main__":
    main()
