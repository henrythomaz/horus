# README — Planejamento do Olavo — Drone e Aquisição de Dados

## Objetivo

Este documento define o planejamento de 15 dias do Olavo dentro do projeto Horus.

A responsabilidade principal do Olavo é a parte relacionada ao **drone, aquisição de imagens, características do voo, georreferenciamento e viabilidade operacional**.

O trabalho dele deve acompanhar a evolução da IA e do backend do Henry. A ideia é que as informações obtidas sobre o drone e sobre a captura de imagens sejam compatíveis com aquilo que o backend precisará receber e armazenar.

---

# Responsabilidades do Olavo

O Olavo será responsável principalmente por:

- estudar o funcionamento e as características dos drones utilizados;
- estudar o dataset utilizado pelo Horus;
- entender as características das imagens aéreas;
- pesquisar altura de voo;
- pesquisar resolução/GSD;
- estudar GPS, latitude e longitude;
- estudar os metadados das imagens;
- pesquisar drones viáveis para o projeto;
- levantar preços e alternativas;
- definir um procedimento de coleta de imagens;
- testar imagens reais quando possível;
- documentar as condições de voo;
- fornecer informações para a integração com o backend;
- ajudar a definir os requisitos necessários para uma missão real.

---

# Relação com o trabalho do Henry

O trabalho do Olavo não precisa esperar o backend ficar pronto.

Durante os primeiros dias, ele deve produzir documentação e informações técnicas que posteriormente serão utilizadas pelo backend.

O objetivo é chegar a uma estrutura semelhante a:

```text
MISSÃO
   ↓
DRONE
   ↓
VOO
   ↓
CAPTURA DE IMAGENS
   ↓
METADADOS
   ↓
IMAGEM
   ↓
LATITUDE
LONGITUDE
ALTITUDE
HORÁRIO
```

Essas informações posteriormente serão utilizadas pelo sistema.

---

# Plano de 15 dias

## Dia 1 — Estudar o dataset utilizado pelo Horus

O primeiro objetivo é entender o dataset utilizado no treinamento.

Pesquisar e documentar:

- origem do dataset;
- artigo/documentação relacionada;
- equipamentos utilizados para captura;
- tipos de drones;
- características das imagens;
- resolução;
- altitude;
- localização;
- condições de captura;
- como as imagens foram processadas;
- como as imagens foram divididas.

O objetivo é responder:

> Em quais condições essas imagens foram obtidas?

### Entrega

Criar:

```text
docs/drone/dataset.md
```

contendo as informações encontradas.

---

# Dia 2 — Estudar os metadados das imagens

Investigar quais informações podem existir nas imagens capturadas por drones.

Pesquisar principalmente:

- EXIF;
- GPS;
- latitude;
- longitude;
- altitude;
- horário;
- orientação da câmera;
- resolução;
- distância focal;
- modelo do equipamento.

Verificar exemplos reais de imagens de drone.

### Entrega

Documentar quais informações podem ser extraídas automaticamente das imagens.

---

# Dia 3 — Estudar altitude de voo

Pesquisar como a altitude influencia a imagem.

Estudar:

```text
altura
 ↓
distância do objeto
 ↓
tamanho aparente do objeto
 ↓
resolução espacial
 ↓
capacidade de detecção
```

Pesquisar diferentes alturas possíveis para o Horus.

Por exemplo:

```text
10 m
20 m
30 m
40 m
50 m
```

Os valores devem ser tratados como hipóteses de teste, não como valores previamente definidos.

### Entrega

Criar:

```text
docs/drone/altitude.md
```

---

# Dia 4 — Estudar GSD e resolução espacial

Estudar o conceito de **Ground Sampling Distance (GSD)**.

O objetivo é entender:

> Quantos centímetros do terreno correspondem a cada pixel da imagem?

Relacionar:

```text
altura
+
câmera
+
distância focal
+
resolução
```

com:

```text
GSD
```

Isso será importante para os experimentos da IA.

### Entrega

Documentar como a resolução espacial pode influenciar a detecção dos objetos.

---

# Dia 5 — Estudar GPS e georreferenciamento

Pesquisar como obter:

```text
latitude
longitude
altitude
```

a partir do drone/imagem.

Estudar:

- GPS;
- GNSS;
- EXIF;
- coordenadas geográficas;
- sistemas de referência;
- precisão do posicionamento.

O objetivo é entender como transformar uma imagem capturada pelo drone em uma informação geográfica utilizável pelo Horus.

### Entrega

Criar:

```text
docs/drone/georeferencing.md
```

---

# Dia 6 — Estudar drones disponíveis

Pesquisar drones que possam ser utilizados no projeto.

Considerar:

- preço;
- disponibilidade no Brasil;
- câmera;
- resolução;
- GPS/GNSS;
- estabilidade;
- autonomia;
- altitude operacional;
- capacidade de registrar coordenadas;
- facilidade de utilização;
- possibilidade de exportar imagens;
- compatibilidade com o objetivo do projeto.

Não procurar necessariamente o drone mais avançado.

A prioridade é encontrar opções:

```text
viável
+
barata
+
capaz de produzir imagens úteis
```

### Entrega

Criar uma tabela comparativa.

Exemplo:

| Drone | Preço | Câmera | GPS | Autonomia | Observações |
|---|---:|---|---|---:|---|
| Modelo A | — | — | — | — | — |
| Modelo B | — | — | — | — | — |
| Modelo C | — | — | — | — | — |

---

# Dia 7 — Definir requisitos mínimos do drone

Com base na pesquisa dos primeiros dias, definir os requisitos mínimos.

Exemplo:

```text
GPS/GNSS
Câmera adequada
Resolução mínima
Autonomia mínima
Estabilidade
Registro de coordenadas
```

Também definir quais características são desejáveis, mas não obrigatórias.

### Entrega

Criar:

```text
docs/drone/requirements.md
```

---

# Dia 8 — Definir metodologia de coleta

Criar o procedimento de captura de imagens que será utilizado no Horus.

Definir:

- área de voo;
- altura;
- velocidade;
- orientação da câmera;
- sobreposição entre imagens;
- iluminação;
- horário preferencial;
- formato das imagens;
- armazenamento;
- identificação das missões.

O procedimento deve ser reproduzível.

Exemplo conceitual:

```text
Denúncia
   ↓
Definir área
   ↓
Planejar voo
   ↓
Executar voo
   ↓
Capturar imagens
   ↓
Salvar imagens + metadados
```

### Entrega

Criar:

```text
docs/drone/collection-methodology.md
```

---

# Dia 9 — Preparar coleta experimental

Preparar uma pequena missão experimental.

O objetivo não é mapear uma cidade inteira.

É produzir um conjunto pequeno de imagens reais para testar o sistema.

Registrar:

```text
data
horário
drone
altura
local
condições climáticas
```

e os arquivos capturados.

### Entrega

Primeiro conjunto experimental de imagens reais, caso seja possível realizar o voo.

---

# Dia 10 — Analisar as imagens reais

Analisar as imagens coletadas.

Verificar:

- qualidade;
- resolução;
- nitidez;
- tamanho dos objetos;
- presença de distorções;
- iluminação;
- sombras;
- quantidade de detalhes;
- presença de informações GPS.

Comparar visualmente com as imagens utilizadas no treinamento.

Uma das perguntas principais será:

> As imagens reais possuem características suficientemente semelhantes às imagens utilizadas para treinar a IA?

### Entrega

Relatório curto da comparação.

---

# Dia 11 — Testar diferentes alturas

Caso seja possível realizar novos voos, capturar imagens em diferentes alturas.

Por exemplo:

```text
altura A
altura B
altura C
```

Não é necessário utilizar exatamente 10, 20, 30, 40 e 50 metros.

O objetivo é obter diferentes níveis de resolução para testar a hipótese.

As imagens devem ser identificadas corretamente.

Exemplo:

```text
mission_001/
├── altitude_10m/
├── altitude_20m/
└── altitude_30m/
```

### Entrega

Conjunto de imagens organizado por altura.

---

# Dia 12 — Trabalhar junto com o Henry

Neste momento o modelo de IA já deverá estar sendo testado pelo Henry.

O Olavo deverá fornecer informações sobre:

- altura;
- localização;
- resolução;
- características da câmera;
- condições de captura;
- origem das imagens.

O objetivo é permitir que o Henry relacione:

```text
imagem
+
altura
+
GSD
+
localização
```

com o resultado da rede neural.

### Entrega

Dataset experimental documentado com os metadados disponíveis.

---

# Dia 13 — Definir o padrão de missão

Definir como uma missão real do Horus deverá funcionar do ponto de vista do drone.

Uma missão deverá possuir informações semelhantes a:

```text
mission
├── identificação
├── data
├── drone
├── piloto
├── área
├── altitude
└── imagens
```

Cada imagem deverá possuir, quando disponível:

```text
filename
latitude
longitude
altitude
captured_at
width
height
```

Essas informações deverão ser compatíveis com o modelo de dados utilizado pelo backend.

### Entrega

Documento:

```text
docs/drone/mission-standard.md
```

---

# Dia 14 — Validar o procedimento de coleta

Revisar todo o procedimento definido.

Verificar se é possível executar uma missão seguindo apenas a documentação.

Checar:

- preparação;
- voo;
- captura;
- armazenamento;
- identificação das imagens;
- obtenção dos metadados;
- organização;
- transferência dos arquivos;
- relação entre imagem e localização.

Corrigir problemas encontrados.

### Entrega

Versão final da metodologia de coleta.

---

# Dia 15 — Consolidar a documentação do drone

Finalizar toda a documentação da parte de drone.

O resultado deverá conter:

```text
docs/drone/
├── dataset.md
├── altitude.md
├── georeferencing.md
├── requirements.md
├── collection-methodology.md
└── mission-standard.md
```

Também entregar:

- tabela de drones avaliados;
- drone recomendado, se houver;
- metodologia de voo;
- metodologia de captura;
- requisitos mínimos;
- informações sobre GPS;
- informações sobre altitude;
- informações sobre GSD;
- conjunto experimental de imagens, se disponível.

---

# Integração com o Backend

As informações produzidas pelo Olavo deverão ser compatíveis com o sistema desenvolvido pelo Henry.

O backend deverá eventualmente receber informações como:

```json
{
  "filename": "image_001.jpg",
  "latitude": -20.784,
  "longitude": -51.700,
  "altitude": 30,
  "captured_at": "2026-08-10T14:30:00",
  "width": 4096,
  "height": 3072
}
```

Essas informações serão utilizadas posteriormente para relacionar:

```text
MISSÃO
   ↓
IMAGEM
   ↓
DETECÇÃO
   ↓
LOCALIZAÇÃO
   ↓
ÁREA DE RISCO
```

---

# Integração com a IA

O trabalho do Olavo também será importante para os experimentos do Henry.

O objetivo é permitir análises como:

```text
Altitude
   ↓
GSD
   ↓
Tamanho aparente do objeto
   ↓
Detecção YOLO
   ↓
Precision / Recall / mAP
```

Dessa maneira, o projeto poderá investigar experimentalmente qual condição de captura produz melhores resultados.

---

# Entrega final do Olavo

Ao final dos 15 dias, o Horus deverá possuir uma metodologia documentada para:

```text
Receber uma denúncia
       ↓
Definir uma área de monitoramento
       ↓
Planejar uma missão
       ↓
Escolher/configurar o drone
       ↓
Realizar o voo
       ↓
Capturar imagens
       ↓
Obter metadados
       ↓
Enviar imagens ao sistema
       ↓
Permitir processamento pela IA
```

O trabalho do Olavo não consiste apenas em "pesquisar drones".

A função dele é estabelecer **como o Horus obterá dados do mundo real de maneira tecnicamente adequada e reproduzível**.

---

# Regra principal

O objetivo não é encontrar o drone perfeito.

O objetivo é descobrir:

> **Qual é a forma mais viável de capturar imagens aéreas que forneçam dados suficientes para o modelo de IA realizar detecções úteis.**

Por isso, as decisões sobre drone, altitude, câmera e metodologia de voo devem ser baseadas nos requisitos do modelo e nos resultados dos experimentos, e não somente nas especificações comerciais dos equipamentos.
