from ultralytics import YOLO

model = YOLO("yolo11n.pt")

model.train(
    data="/home/henry/projetos/horus/datasets/DATASET.yolov8/data.yaml",
    epochs=10,
    imgsz=320,
    batch=4,
    device="cpu",
    project="runs",
    name="horus_mvp"
)
