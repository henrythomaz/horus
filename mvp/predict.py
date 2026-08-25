from ultralytics import YOLO
import sys

if len(sys.argv) < 2:
    print("Erro: Você deve passar o caminho da imagem!")
    print("Uso correto: python predict.py tests/DJI_012.jpg")
    sys.exit(1)

IMAGEM_REQUISITADA = sys.argv[1]

MODEL = "../runs/detect/runs/horus_mvp-5/weights/best.pt"

model = YOLO(MODEL)

results = model.predict(
    source=IMAGEM_REQUISITADA,
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
