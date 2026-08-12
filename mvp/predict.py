from ultralytics import YOLO

MODEL = "../runs/detect/runs/horus_mvp-3/weights/best.pt"

model = YOLO(MODEL)

results = model.predict(
    source="tests/DJI_012.jpg",
    conf=0.25,
    save=True
)

names = model.names

for result in results:
    for box in result.boxes:
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])

        print(
            f"Classe: {names[class_id]}\n"
            f"Confiança: {confidence:.2f}"
        )
