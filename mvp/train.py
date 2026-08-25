from ultralytics import YOLO

model = YOLO("yolo11l.pt")

model.train(
    data="/home/henry/projetos/horus/datasets/DATASET.yolov8/data.yaml",
    epochs=50,
    imgsz=1280,
    batch=8,
    device="cpu",
    project="runs",
    name="horus_640_50"
)
