from ultralytics import YOLO

model = YOLO("yolo11n.pt")

model.train(
    data="/home/henry/projetos/horus/datasets/DATASET.yolov8/data.yaml",
    epochs=50,
    imgsz=640,
    batch=4,
    device="cpu",
    project="runs",
    name="horus_640_50"
)
