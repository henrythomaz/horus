# Horus --- Sistema Inteligente de Detecção de Focos de Dengue por Imagens Aéreas

## 1. Visão geral

O **Horus** é uma plataforma de visão computacional e inteligência
artificial destinada a auxiliar equipes de vigilância e controle de
zoonoses na identificação de **possíveis focos de proliferação do Aedes
aegypti** a partir de imagens aéreas capturadas por drones.

O sistema não parte do princípio de que toda a cidade já foi mapeada.

O fluxo principal começa com uma **denúncia ou solicitação de
inspeção**. A partir dela, uma equipe realiza uma missão com drone na
região indicada. As imagens capturadas são processadas por um modelo de
detecção de objetos, que identifica elementos potencialmente associados
a criadouros. Essas detecções são posteriormente utilizadas para gerar
áreas de risco, mapas e relatórios que auxiliam a equipe de campo a
decidir onde realizar uma inspeção presencial.

### Fluxo principal

``` text
Denúncia
   ↓
Missão de inspeção
   ↓
Voo do drone
   ↓
Imagens georreferenciadas
   ↓
Modelo de IA
   ↓
Predições
   ↓
Análise espacial
   ↓
Áreas de risco
   ↓
Mapa + relatório
   ↓
Inspeção da equipe de zoonoses
```

O projeto possui também uma segunda parte, responsável pelo
**desenvolvimento e avaliação dos modelos de inteligência artificial**.
Essa parte utiliza datasets anotados, como datasets exportados em
formato YOLO, para treinar e avaliar os modelos.

------------------------------------------------------------------------

# 2. Princípio arquitetural

O banco de dados do Horus separa dois contextos:

1.  **Operação do sistema** --- dados gerados durante as missões reais.
2.  **Desenvolvimento da IA** --- datasets, anotações, modelos e
    execuções de treinamento.

Essa separação é importante porque uma imagem usada para treinar a rede
neural não é a mesma coisa que uma imagem capturada durante uma missão
real.

``` text
                 HORUS
                   │
       ┌───────────┴───────────┐
       │                       │
       ▼                       ▼
 OPERAÇÃO DO SISTEMA      DESENVOLVIMENTO DA IA
       │                       │
       ▼                       ▼
 organizações             datasets
 usuários                 dataset_images
 denúncias                dataset_annotations
 missões                  classes
 imagens                  models
 predições                model_runs
 áreas de risco
 relatórios
```

------------------------------------------------------------------------

# 3. Fluxo operacional

## 3.1 Organização

Uma organização representa uma instituição que utiliza o Horus.

Exemplos:

-   Prefeitura de Três Lagoas;
-   Centro de Controle de Zoonoses;
-   Secretaria Municipal de Saúde.

Uma organização pode possuir vários usuários.

``` text
organizations
       │
       └── users
```

------------------------------------------------------------------------

## 3.2 Usuários

Os usuários representam as pessoas que utilizam o sistema.

Exemplos de funções:

-   `admin` --- administrador da organização;
-   `agent` --- agente de zoonoses;
-   `operator` --- operador do sistema/drone;
-   `analyst` --- analista responsável pela análise dos resultados.

Cada usuário pertence a uma organização.

### Tabela: `users`

  Campo               Função
  ------------------- ----------------------------------
  `id`                Identificador do usuário
  `organization_id`   Organização à qual pertence
  `name`              Nome
  `email`             E-mail
  `password_hash`     Senha armazenada de forma segura
  `role`              Função do usuário
  `created_at`        Data de criação

------------------------------------------------------------------------

# 4. Denúncias

## 4.1 Por que existe a tabela `complaints`?

O fluxo real do Horus começa com uma solicitação de investigação.

Por exemplo:

> Um morador denuncia que existe um terreno com possíveis recipientes
> acumulando água no bairro X.

Essa denúncia precisa ser registrada antes da missão.

A denúncia pode possuir uma localização aproximada, mas essa localização
**não representa necessariamente todas as imagens que serão
capturadas**.

### Tabela: `complaints`

  Campo               Função
  ------------------- ---------------------------
  `id`                Identificador da denúncia
  `organization_id`   Organização responsável
  `reported_by`       Usuário que registrou
  `description`       Descrição da denúncia
  `neighborhood`      Bairro
  `address`           Endereço
  `latitude`          Latitude informada
  `longitude`         Longitude informada
  `status`            Estado da denúncia
  `created_at`        Data de criação
  `resolved_at`       Data de resolução

### Exemplo

``` text
Denúncia #42

Bairro: Jardim X
Descrição: possível acúmulo de recipientes com água
Latitude: -20.xxxxx
Longitude: -51.xxxxx
Status: pending
```

------------------------------------------------------------------------

# 5. Missões

Uma missão representa uma operação de campo realizada para investigar
uma denúncia.

Uma denúncia pode originar uma ou mais missões.

``` text
complaint
     │
     └────── N missions
```

Isso é importante porque uma denúncia pode precisar ser investigada
novamente.

Por exemplo:

``` text
Denúncia #42
   │
   ├── Missão #100 — primeira inspeção
   │
   └── Missão #145 — nova inspeção
```

### Tabela: `missions`

  Campo               Função
  ------------------- ----------------------------
  `id`                Identificador
  `organization_id`   Organização responsável
  `complaint_id`      Denúncia investigada
  `pilot_id`          Usuário/piloto responsável
  `name`              Nome da missão
  `started_at`        Início
  `finished_at`       Final
  `altitude`          Altitude de voo
  `status`            Estado da missão
  `created_at`        Criação

### Estados possíveis

``` text
planned
in_progress
completed
canceled
```

------------------------------------------------------------------------

# 6. Imagens

Durante uma missão, o drone captura várias imagens.

Cada imagem pertence a uma missão:

``` text
mission
   │
   └──── N images
```

### Tabela: `images`

  Campo           Função
  --------------- -----------------------------
  `id`            Identificador
  `mission_id`    Missão responsável
  `filename`      Nome do arquivo
  `path`          Localização do arquivo
  `latitude`      Latitude da captura
  `longitude`     Longitude da captura
  `altitude`      Altitude da captura
  `captured_at`   Momento da captura
  `width`         Largura
  `height`        Altura
  `processed`     Indica se já foi processada
  `created_at`    Data de cadastro

## Georreferenciamento

As coordenadas de uma imagem operacional devem vir, quando disponíveis,
dos dados do voo/drone, como:

-   GPS;
-   EXIF;
-   telemetria;
-   logs do voo;
-   RTK;
-   outros metadados geoespaciais.

É importante não assumir que datasets públicos possuem essas
informações.

O dataset utilizado para treinamento pode conter apenas imagens e
anotações. Já as imagens capturadas durante uma missão real devem ser
associadas às informações geográficas disponíveis.

------------------------------------------------------------------------

# 7. Classes de detecção

As classes representam os tipos de objetos que o modelo pode
identificar.

### Tabela: `detection_classes`

  Campo           Função
  --------------- ------------------------------------
  `id`            Identificador da classe
  `name`          Nome
  `description`   Descrição
  `risk_weight`   Peso utilizado na análise de risco
  `created_at`    Data de criação

O campo `risk_weight` permite que o cálculo de risco seja ajustado
posteriormente.

## Classes iniciais do dataset

O dataset atualmente analisado possui:

``` text
0 → cocunut_shell
1 → drum
2 → other_containers
3 → tire
4 → water_tank
```

Essas classes representam **as categorias existentes no dataset
utilizado**, e não necessariamente as classes definitivas do Horus.

A definição final das classes deverá ser baseada em literatura, dados
reais, qualidade das anotações e capacidade de identificação a partir
das imagens aéreas.

------------------------------------------------------------------------

# 8. Dataset de treinamento

O dataset usado para desenvolver a IA é separado das imagens de missões
reais.

### Tabela: `datasets`

Representa um conjunto de dados.

  Campo           Função
  --------------- -----------------
  `id`            Identificador
  `name`          Nome do dataset
  `version`       Versão
  `description`   Descrição
  `created_at`    Data de criação

Exemplo:

``` text
Aedes Breeding Habitat
v1
```

------------------------------------------------------------------------

# 9. Imagens do dataset

### Tabela: `dataset_images`

Representa as imagens utilizadas no processo de treinamento e avaliação.

  Campo          Função
  -------------- --------------------------
  `id`           Identificador
  `dataset_id`   Dataset ao qual pertence
  `filename`     Nome da imagem
  `path`         Caminho
  `split`        train, valid ou test
  `width`        Largura
  `height`       Altura

## Divisão do dataset

### `train`

Imagens utilizadas para **treinar** os parâmetros do modelo.

### `valid`

Imagens utilizadas durante o desenvolvimento para avaliar o
comportamento do modelo e auxiliar na escolha de configurações.

### `test`

Imagens reservadas para a **avaliação final**.

A separação é importante porque utilizar as mesmas imagens para
treinamento e avaliação pode gerar resultados artificialmente bons.

------------------------------------------------------------------------

# 10. Anotações do dataset

Os arquivos `.txt` do formato YOLO representam as anotações das imagens.

Exemplo:

``` text
4 0.750566 0.335527 0.167402 0.135332
```

A estrutura é:

``` text
class_id
x_center
y_center
width
height
```

Os valores de posição e tamanho são normalizados entre `0` e `1`.

### Tabela: `dataset_annotations`

  Campo                Função
  -------------------- ---------------------
  `id`                 Identificador
  `dataset_image_id`   Imagem anotada
  `class_id`           Classe do objeto
  `x_center`           Centro X
  `y_center`           Centro Y
  `width`              Largura normalizada
  `height`             Altura normalizada

Assim, o script de importação do dataset poderá transformar:

``` text
train/images/DJI_0001.jpg
train/labels/DJI_0001.txt
```

em registros no banco:

``` text
datasets
      ↓
dataset_images
      ↓
dataset_annotations
      ↓
detection_classes
```

------------------------------------------------------------------------

# 11. Modelos de IA

### Tabela: `models`

Representa uma versão de um modelo treinado.

  Campo          Função
  -------------- -------------------------------
  `id`           Identificador
  `name`         Nome do modelo
  `version`      Versão
  `task`         Tarefa, como object detection
  `path`         Local do arquivo do modelo
  `created_at`   Data de criação

Exemplos:

``` text
YOLO
YOLO11
RT-DETR
```

O projeto pode comparar arquiteturas diferentes.

------------------------------------------------------------------------

# 12. Execuções de treinamento

Um mesmo modelo pode ser treinado diversas vezes com diferentes
datasets, hiperparâmetros ou versões.

Por isso existe `model_runs`.

### Tabela: `model_runs`

  Campo           Função
  --------------- ----------------------
  `id`            Identificador
  `model_id`      Modelo utilizado
  `dataset_id`    Dataset utilizado
  `started_at`    Início
  `finished_at`   Final
  `metrics`       Métricas da execução

As métricas podem armazenar informações como:

``` text
precision
recall
mAP@50
mAP@50-95
F1
```

Isso permite comparar diferentes experimentos.

------------------------------------------------------------------------

# 13. Predições

Depois que um modelo treinado recebe uma imagem de uma missão, ele
produz predições.

``` text
images
   │
   ▼
modelo
   │
   ▼
predictions
```

### Tabela: `predictions`

  Campo            Função
  ---------------- ---------------------------
  `id`             Identificador
  `image_id`       Imagem analisada
  `model_run_id`   Modelo/execução utilizada
  `class_id`       Classe detectada
  `confidence`     Confiança da detecção
  `x_center`       Centro X
  `y_center`       Centro Y
  `width`          Largura
  `height`         Altura
  `created_at`     Data

Exemplo:

``` text
Imagem: DJI_0001.jpg

Classe: tire
Confiança: 0.91

Bounding box:
x_center = ...
y_center = ...
width = ...
height = ...
```

------------------------------------------------------------------------

# 14. Ground truth x Prediction

É fundamental diferenciar:

### Ground truth

Aquilo que foi anotado no dataset.

``` text
dataset_annotations
```

### Prediction

Aquilo que o modelo acredita ter encontrado.

``` text
predictions
```

Essa separação permite avaliar o modelo corretamente.

Por exemplo:

``` text
Ground truth
      ↕
comparação
      ↕
Prediction
```

A partir dessa comparação podem ser calculadas métricas como:

-   Precision;
-   Recall;
-   F1;
-   IoU;
-   mAP@50;
-   mAP@50-95.

------------------------------------------------------------------------

# 15. Áreas de risco

Uma detecção individual não necessariamente representa uma área de
risco.

Imagine:

``` text
Pneu
Pneu
Recipiente
Caixa d'água
```

encontrados próximos uns dos outros.

Essas detecções podem ser agrupadas espacialmente em uma área de
interesse.

### Tabela: `risk_areas`

  Campo          Função
  -------------- --------------------
  `id`           Identificador
  `mission_id`   Missão
  `latitude`     Latitude central
  `longitude`    Longitude central
  `radius`       Raio da área
  `risk_score`   Pontuação de risco
  `created_at`   Data

A área de risco representa uma **região que merece atenção**, e não uma
afirmação de que existe necessariamente um foco epidemiológico
confirmado.

------------------------------------------------------------------------

# 16. Pontuação de risco

O Horus poderá gerar uma pontuação de risco, por exemplo:

``` text
0 – 19     Muito baixo
20 – 39    Baixo
40 – 59    Moderado
60 – 79    Alto
80 – 100   Muito alto
```

Essa pontuação não deve ser interpretada automaticamente como
"probabilidade de dengue".

Ela representa uma **pontuação de prioridade/risco definida pelo
sistema**, baseada nas evidências disponíveis.

O cálculo poderá considerar:

-   quantidade de objetos detectados;
-   tipo dos objetos;
-   confiança das detecções;
-   proximidade espacial;
-   concentração de possíveis criadouros;
-   características da imagem;
-   histórico de inspeções;
-   dados ambientais, futuramente.

------------------------------------------------------------------------

# 17. Relatórios

### Tabela: `reports`

Um relatório representa o resultado consolidado de uma missão.

  Campo            Função
  ---------------- ---------------------
  `id`             Identificador
  `mission_id`     Missão
  `generated_by`   Usuário responsável
  `file_path`      Arquivo gerado
  `generated_at`   Data de geração
  `created_at`     Data de criação

Um relatório poderá conter:

``` text
Resumo da missão
Quantidade de imagens
Quantidade de detecções
Classes encontradas
Áreas de risco
Pontuações
Mapa
Imagens relevantes
Informações da missão
```

------------------------------------------------------------------------

# 18. Fluxo completo de produção

O fluxo esperado para uma utilização real é:

``` text
                    USUÁRIO
                       │
                       ▼
                  NOVA DENÚNCIA
                       │
                       ▼
                  COMPLAINT
                       │
                       ▼
                    MISSÃO
                       │
                       ▼
                 VOO DO DRONE
                       │
                       ▼
            IMAGENS + GPS + METADADOS
                       │
                       ▼
                  PRÉ-PROCESSAMENTO
                       │
                       ▼
                    MODELO YOLO
                       │
                       ▼
                   PREDICTIONS
                       │
                       ▼
              ANÁLISE ESPACIAL
                       │
                       ▼
                 RISK AREAS
                       │
                 ┌─────┴─────┐
                 ▼           ▼
               MAPA       RELATÓRIO
                 │           │
                 └─────┬─────┘
                       ▼
               AGENTE DE CAMPO
                       │
                       ▼
             INSPEÇÃO PRESENCIAL
```

------------------------------------------------------------------------

# 19. Fluxo de desenvolvimento da IA

Separadamente, o desenvolvimento do modelo segue:

``` text
Dataset público / próprio
          │
          ▼
     Organização
          │
          ▼
       Anotação
          │
          ▼
 train / valid / test
          │
          ▼
       YOLO / outro
          │
          ▼
      Treinamento
          │
          ▼
     model_runs
          │
          ▼
       Avaliação
          │
          ▼
     Modelo aprovado
          │
          ▼
      Deploy da IA
```

------------------------------------------------------------------------

# 20. Importação do dataset YOLO

O projeto deverá possuir um script responsável por transformar o dataset
em registros no PostgreSQL.

Estrutura típica:

``` text
dataset/
├── train/
│   ├── images/
│   └── labels/
├── valid/
│   ├── images/
│   └── labels/
└── test/
    ├── images/
    └── labels/
```

O script:

``` text
import_yolo_dataset.py
```

deverá:

1.  Criar ou localizar o dataset;
2.  Ler as imagens;
3.  Registrar `train`, `valid` e `test`;
4.  Localizar o `.txt` correspondente;
5.  Ler cada anotação;
6.  Associar a anotação à classe;
7.  Inserir a anotação no PostgreSQL.

Exemplo:

``` text
DJI_0001.jpg
DJI_0001.txt
```

vira:

``` text
dataset_images
       │
       └── dataset_annotations
                  │
                  └── detection_classes
```

------------------------------------------------------------------------

# 21. Por que não usar `images` para o dataset?

A tabela `images` pertence ao contexto operacional.

Ela representa:

> "Esta imagem foi capturada durante uma missão."

Já `dataset_images` representa:

> "Esta imagem faz parte de um dataset utilizado no desenvolvimento da
> IA."

São conceitos diferentes.

Isso permite que o sistema mantenha:

``` text
Imagens de treinamento
        ≠
Imagens de missões reais
```

sem misturar os dados.

------------------------------------------------------------------------

# 22. Por que não usar `detections` para tudo?

O projeto deve separar:

``` text
dataset_annotations
```

de:

``` text
predictions
```

porque são informações de naturezas diferentes.

### Dataset annotation

É a resposta esperada.

``` text
"Existe um pneu aqui."
```

### Prediction

É a resposta produzida pelo modelo.

``` text
"Acredito que existe um pneu aqui com confiança 91%."
```

Essa distinção é essencial para a avaliação científica.

------------------------------------------------------------------------

# 23. Geoprocessamento

O Horus possui uma etapa espacial porque as imagens das missões podem
possuir coordenadas.

A partir das coordenadas será possível futuramente:

-   posicionar imagens no mapa;
-   posicionar detecções;
-   agrupar detecções próximas;
-   criar áreas de risco;
-   gerar mapas de calor;
-   priorizar inspeções;
-   calcular distâncias;
-   relacionar resultados com bairros.

A stack prevista inclui:

``` text
PostgreSQL
PostGIS
GeoPandas
Shapely
Rasterio
```

As coordenadas geográficas deverão utilizar um sistema de referência
adequado, inicialmente **WGS84 / EPSG:4326** para latitude e longitude.

------------------------------------------------------------------------

# 24. Arquitetura de software

A arquitetura inicial prevista é:

``` text
                    ┌──────────────┐
                    │    React     │
                    │    Vite      │
                    └──────┬───────┘
                           │
                           │ HTTP
                           ▼
                    ┌──────────────┐
                    │   FastAPI    │
                    └──────┬───────┘
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
        PostgreSQL       YOLO         Serviços
        + PostGIS        PyTorch      auxiliares
             │             │
             │             ▼
             │         Predictions
             │
             ▼
        Dados geográficos
```

------------------------------------------------------------------------

# 25. Tecnologias

## Inteligência Artificial

-   Python
-   PyTorch
-   Torchvision
-   Ultralytics YOLO
-   Albumentations
-   NumPy
-   OpenCV

## Geoprocessamento

-   GeoPandas
-   Shapely
-   Rasterio
-   PostGIS

## Backend

-   FastAPI
-   Pydantic
-   SQLAlchemy
-   Psycopg
-   Uvicorn

## Frontend

-   React
-   Vite

## Infraestrutura

-   Docker
-   Docker Compose
-   PostgreSQL
-   Git
-   GitHub
-   GitHub Actions

## Configuração

-   python-dotenv

------------------------------------------------------------------------

# 26. Estrutura conceitual do banco

``` text
ORGANIZAÇÃO
│
├── USERS
│
├── COMPLAINTS
│      │
│      └── MISSIONS
│             │
│             ├── IMAGES
│             │      │
│             │      └── PREDICTIONS
│             │
│             ├── RISK_AREAS
│             │
│             └── REPORTS
│
└── ...


DESENVOLVIMENTO DA IA

DATASETS
│
└── DATASET_IMAGES
       │
       └── DATASET_ANNOTATIONS
                  │
                  └── DETECTION_CLASSES

MODELS
│
└── MODEL_RUNS
       │
       └── DATASETS
```

------------------------------------------------------------------------

# 27. Princípios importantes do projeto

## 27.1 O sistema não confirma dengue

O modelo não detecta diretamente a doença dengue.

Ele identifica **objetos ou condições visíveis nas imagens que podem
estar associados a potenciais criadouros**.

Portanto, o resultado deve ser tratado como:

> **apoio à vigilância e priorização de inspeções.**

A confirmação deve continuar sendo realizada pela equipe responsável.

------------------------------------------------------------------------

## 27.2 Imagens aéreas são diferentes de imagens comuns

Um dos principais desafios científicos do Horus é a diferença entre:

-   altura do drone;
-   resolução espacial;
-   GSD;
-   iluminação;
-   ângulo da câmera;
-   tamanho aparente dos objetos;
-   sombras;
-   oclusões;
-   condições meteorológicas;
-   tipo de drone/câmera.

Por isso, um dataset com imagens bonitas e muito semelhantes não é
suficiente para provar que o modelo funcionará em campo.

O projeto deverá avaliar a capacidade de generalização para imagens
reais.

------------------------------------------------------------------------

## 27.3 Evitar vazamento entre train, validation e test

Imagens quase idênticas, provenientes da mesma captura ou do mesmo
local, não devem ser distribuídas aleatoriamente entre treino e teste.

Caso isso aconteça, o modelo pode memorizar características da cena e
apresentar uma métrica artificialmente alta.

Sempre que possível, a divisão deve considerar:

-   voo;
-   local;
-   sequência de captura;
-   área geográfica.

------------------------------------------------------------------------

# 28. Validação científica

O desempenho do modelo deverá ser medido com dados que não participaram
do treinamento.

As principais métricas serão:

``` text
Precision
Recall
F1 Score
mAP@50
mAP@50-95
IoU
```

Além disso, o Horus deverá avaliar:

``` text
altura de voo
      ×
GSD
      ×
desempenho da detecção
```

Isso permitirá investigar qual altura/resolução oferece melhor
equilíbrio entre cobertura e capacidade de identificação.

------------------------------------------------------------------------

# 29. Evolução futura

O sistema poderá posteriormente incorporar:

-   processamento de vídeos;
-   monitoramento temporal;
-   rotas automáticas de inspeção;
-   aplicativo móvel para agentes;
-   integração com dados meteorológicos;
-   previsão de áreas críticas;
-   análise de séries temporais;
-   integração com sistemas municipais;
-   ortomosaicos;
-   modelos de segmentação;
-   modelos multimodais/LLMs para geração de relatórios;
-   histórico de inspeções;
-   confirmação de campo para realimentar o dataset.

------------------------------------------------------------------------

# 30. Estado esperado do MVP

A primeira versão funcional do Horus deverá conseguir:

``` text
1. Registrar uma organização
2. Registrar usuários
3. Registrar uma denúncia
4. Criar uma missão
5. Associar imagens à missão
6. Processar imagens com o modelo
7. Registrar predições
8. Associar coordenadas às imagens
9. Gerar áreas de risco
10. Exibir as áreas em um mapa
11. Gerar um relatório
```

Paralelamente, o ambiente de desenvolvimento da IA deverá permitir:

``` text
1. Importar dataset YOLO
2. Registrar train/valid/test
3. Importar labels dos arquivos .txt
4. Registrar classes
5. Treinar modelos
6. Registrar experimentos
7. Avaliar métricas
8. Versionar modelos
```

------------------------------------------------------------------------

# 31. Resumo

O Horus foi projetado para funcionar como um ciclo:

``` text
                 ┌───────────────┐
                 │    DENÚNCIA   │
                 └───────┬───────┘
                         ▼
                 ┌───────────────┐
                 │    MISSÃO     │
                 └───────┬───────┘
                         ▼
                 ┌───────────────┐
                 │    DRONE      │
                 └───────┬───────┘
                         ▼
                 ┌───────────────┐
                 │    IMAGENS    │
                 └───────┬───────┘
                         ▼
                 ┌───────────────┐
                 │      IA       │
                 └───────┬───────┘
                         ▼
                 ┌───────────────┐
                 │  PREDIÇÕES    │
                 └───────┬───────┘
                         ▼
                 ┌───────────────┐
                 │ ÁREAS DE RISCO│
                 └───────┬───────┘
                         ▼
                 ┌───────────────┐
                 │ MAPA/RELATÓRIO│
                 └───────┬───────┘
                         ▼
                 ┌───────────────┐
                 │ INSPEÇÃO      │
                 │   HUMANA      │
                 └───────┬───────┘
                         │
                         ▼
                  NOVOS DADOS
                         │
                         ▼
                  MELHORIA DA IA
```

O objetivo final é criar um sistema em que **a inteligência artificial
reduza o espaço de busca da equipe de zoonoses**, direcionando os
agentes para locais que apresentam maior evidência de possíveis
criadouros, sem substituir a inspeção e a validação humana.
