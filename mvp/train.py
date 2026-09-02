from ultralytics import YOLO


def main():
    model = YOLO("yolo11m.pt")

    model.train(
        data="/home/henry/projetos/horus/datasets/DATASET.yolov8/data.yaml",
        epochs=50,
        imgsz=640,
        batch=8,
        device=0,
        workers=0,
        project="runs",
        name="horus_640_50"
    )

if __name__ == "__main__":
    main()
