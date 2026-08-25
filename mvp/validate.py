from ultralytics import YOLO

model = YOLO("../runs/detect/runs/horus_640_50/weights/best.pt")

metrics = model.val(
        data="/home/henry/projetos/horus/datasets/DATASET.yolov8/data.yaml",
        split="test"
)

print("mAP50:", metrics.box.map50)
print("mAP50-95:", metrics.box.map)
