# Resultado do MVP

## Modelo

YOLO11n

## Dataset

Treino: 1975 imagens
Validação: 423 imagens
Teste: 423 imagens

## Classes

- cocunut_shell
- drum
- other_containers
- tire
- water_tank

## Treinamento

Épocas: 10
Imagem: 320x320
Hardware: AMD Ryzen 5 PRO 3500U
GPU: não utilizada

## Teste

Precision: 0.696
Recall: 0.663
mAP@50: 0.666
mAP@50-95: 0.461

## Conclusão

O MVP demonstrou que o modelo consegue realizar
detecção das classes presentes no dataset e realizar
inferência em imagens não utilizadas diretamente
durante o treinamento.

O modelo ainda não deve ser considerado adequado
para operação real. É necessário ampliar e melhorar
o dataset e realizar novos treinamentos com imagens
aéreas representativas do cenário de utilização.
