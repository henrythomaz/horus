# Relatório de Treinamento – YOLO11l (1280px)

## Modelo

**YOLO11l** – arquitetura Large, com aproximadamente 25,3 milhões de parâmetros.  
Substitui o YOLO11n (2,6M) para maior capacidade de aprendizado e melhor detecção de objetos pequenos.

## Dataset

Mesmo dataset utilizado no MVP:

| Divisão  | Quantidade |
|----------|------------|
| Treino   | 1975       |
| Validação| 423        |
| Teste    | 423        |

## Classes

As mesmas 5 classes:

- coconut_shell  
- drum  
- other_containers  
- tire  
- water_tank  

## Configuração de Treinamento

| Parâmetro       | Valor          | Observação                                               |
|-----------------|----------------|----------------------------------------------------------|
| Épocas          | 50             | Número suficiente para convergência (monitorar overfitting)|
| Tamanho da imagem (`imgsz`) | 1280  | Resolução mais alta para capturar detalhes finos         |
| Batch size      | 8              | Ajustado para melhor uso da memória da GPU               |
| Dispositivo     | GPU (a definir)| O treinamento será realizado em outro computador com GPU |
| Otimizador      | Auto (SGD)     | Padrão do YOLO                                           |
| Augmentations   | Padrão         | Inclui mosaic, HSV, translate, scale, flip, etc.         |

## Expectativas de Desempenho

Com base em experimentos documentados e na literatura do YOLO, espera‑se:

- **mAP50** > 0,85 (contra 0,666 do MVP)  
- **mAP50-95** > 0,70 (contra 0,461 do MVP)  
- Melhoria significativa na detecção de objetos pequenos e nas classes com menor recall (ex: *drum*, *other_containers*).

Esses ganhos são atribuídos ao:
- Modelo mais profundo (YOLO11l);
- Resolução mais alta (1280×1280);
- Número maior de épocas (50 vs 10).

## Validação Pós‑Treino

Após o treinamento, serão realizadas:

- Validação no conjunto de teste para obter as métricas oficiais;
- Análise por classe para identificar possíveis fragilidades;
- Inferência em imagens reais (aéreas) com diferentes condições de iluminação e distância.

## Ajustes na Inferência

No script `predict.py`, o limiar de confiança (`conf`) foi reduzido de **0,25** para **0,15** para capturar mais detecções verdadeiras, mesmo com confiança moderada. Esse valor pode ser reajustado após a validação.

## Conclusão

Este novo treinamento representa um avanço significativo em relação ao MVP, tanto em termos de arquitetura quanto de resolução. Espera‑se que o modelo resultante atinja um nível de precisão adequado para testes em campo. 

Os resultados concretos (métricas, curvas, matriz de confusão) serão anexados após a conclusão do treinamento.

---

**Data do relatório:** 25/08/2026  
**Responsável:** Henry
