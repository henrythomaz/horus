
# Relatório de Treinamento – YOLO11l (1280px)

## Modelo

YOLO11l – arquitetura Large, com aproximadamente 25,3 milhões de parâmetros.

O modelo foi utilizado com o objetivo de aumentar a capacidade de detecção em relação ao YOLO11n empregado no MVP anterior, especialmente em objetos de menor dimensão.

## Dataset

Mesmo dataset utilizado no MVP:

Treino: 1975 imagens
Validação: 423 imagens
Teste: 423 imagens

## Classes

* coconut_shell
* drum
* other_containers
* tire
* water_tank

## Treinamento

Épocas: 50
Tamanho da imagem: 1280×1280
Batch size: 2
Dispositivo: NVIDIA GeForce RTX 4050 Laptop GPU
VRAM disponível: aproximadamente 6 GB
Workers: 0
Otimizador: AdamW (selecionado automaticamente pelo Ultralytics)
Augmentations: configurações padrão do Ultralytics

Durante o treinamento, a configuração inicialmente utilizada com batch size 4 excedeu a memória disponível da GPU. O treinamento foi então continuado com batch size 2.

## Resultados

Os resultados apresentados abaixo correspondem ao conjunto de **validação**, utilizado durante o treinamento.

Melhor mAP@50: 0.739
Melhor mAP@50-95: 0.557

Na época 48 foram obtidos:

Precision: 0.736
Recall: 0.695
mAP@50: 0.739
mAP@50-95: 0.549

Na época 50, o treinamento terminou com:

Precision: 0.682
Recall: 0.728
mAP@50: 0.733
mAP@50-95: 0.553

## Comparação com o MVP anterior

O MVP anterior, baseado no YOLO11n, apresentou:

Precision: 0.696
Recall: 0.663
mAP@50: 0.666
mAP@50-95: 0.461

O novo treinamento apresentou melhora nas métricas de mAP do conjunto de validação, alcançando aproximadamente:

mAP@50: 0.739
mAP@50-95: 0.557

Em comparação com o MVP anterior, isso representa uma melhoria aproximada de:

+10,9% em mAP@50
+20,8% em mAP@50-95

## Análise das Inferências

Testes realizados em imagens aéreas reais do drone demonstraram que o modelo consegue detectar diferentes classes do dataset, porém apresenta dificuldades de generalização em algumas situações.

Foram observados:

* confusão entre as classes `drum` e `water_tank`;
* confusão entre `tire` e `other_containers`;
* dificuldade na detecção de objetos pequenos;
* ocorrência de falsos positivos em alguns objetos que não pertencem às classes do dataset;
* redução significativa da confiança em determinadas imagens aéreas.

Em alguns casos, previsões de baixa confiança somente apareceram quando o limiar de confiança foi reduzido durante os testes.

## Avaliação

Os resultados de validação indicam uma evolução significativa em relação ao MVP anterior. Entretanto, o comportamento observado nas imagens aéreas reais demonstra que o desempenho ainda não é suficientemente consistente para considerar o modelo adequado para operação em campo.

As principais limitações observadas estão relacionadas à generalização para diferentes condições das imagens aéreas e à separação entre classes visualmente semelhantes.

## Próximos Passos

Antes de realizar novos treinamentos, serão realizadas:

* avaliação do `best.pt` no conjunto de teste;
* comparação com modelos anteriores nas mesmas imagens aéreas;
* análise de desempenho por classe;
* análise da matriz de confusão;
* investigação da distribuição das classes no dataset;
* avaliação de novas estratégias de treinamento e de modelos YOLO de diferentes tamanhos.

Também será avaliada a inclusão de imagens aéreas reais devidamente anotadas no dataset, visando aproximar o conjunto de treinamento das condições reais de utilização do sistema Horus.

## Conclusão

O treinamento com YOLO11l em resolução de 1280×1280 apresentou melhora significativa em relação ao MVP anterior nas métricas de validação, especialmente em mAP@50 e mAP@50-95.

Apesar dos resultados positivos no conjunto de validação, os testes em imagens aéreas reais indicam que o modelo ainda apresenta inconsistências na detecção e classificação de determinadas classes. Dessa forma, o modelo representa uma evolução do MVP, mas ainda requer novos experimentos e melhorias no conjunto de dados antes de ser considerado adequado para utilização em campo.

---

Data do relatório: 01/09/2026
Responsável: Henry
