# Horus - Sistema Inteligente de Detecção de Focos de Dengue por Imagens Aéreas

## Visão Geral

Este projeto tem como objetivo desenvolver uma plataforma capaz de identificar possíveis focos de proliferação do mosquito Aedes aegypti a partir de imagens capturadas por drones, utilizando técnicas de Visão Computacional e Deep Learning.

A solução busca auxiliar Centros de Controle de Zoonoses, Secretarias Municipais de Saúde e Prefeituras na priorização de inspeções, redução de custos operacionais e aumento da eficiência no combate à dengue.

---

# Problema

O combate à dengue ainda depende fortemente de inspeções manuais realizadas por agentes de saúde.

Esse processo apresenta diversas limitações:

- Grande demanda de mão de obra.
- Alto custo operacional.
- Cobertura limitada do território.
- Dificuldade de localizar rapidamente possíveis criadouros.

Com o crescimento dos casos de dengue em diversas regiões do Brasil, torna-se necessária a adoção de ferramentas tecnológicas que permitam identificar áreas de risco de forma mais eficiente.

---

# Hipótese

É possível utilizar imagens aéreas obtidas por drones e modelos de Deep Learning para detectar objetos e condições associadas à proliferação do mosquito da dengue, gerando mapas de risco que auxiliem equipes de fiscalização e controle epidemiológico.

---

# Objetivos

## Objetivo Geral

Desenvolver um sistema inteligente capaz de detectar potenciais focos de dengue em imagens aéreas e gerar informações georreferenciadas para apoio à tomada de decisão.

## Objetivos Específicos

## Objetivos Específicos

- Consumir um banco de imagens aéreas da cidade.
- Estudar métodos de detecção de objetos utilizando Deep Learning.
- Anotar e organizar um dataset para treinamento.
- Treinar modelos capazes de identificar possíveis criadouros.
- Avaliar o desempenho dos modelos.
- Determinar a altura ótima de voo para maximizar a confiabilidade das detecções.
- Avaliar a influência da resolução espacial (GSD) na identificação de possíveis focos.
- Comparar o desempenho de diferentes arquiteturas de detecção de objetos.
- Desenvolver uma API para inferência.
- Desenvolver uma interface web para visualização dos resultados.
- Gerar mapas de risco e relatórios automáticos.
- Georreferenciar as detecções realizadas pelo modelo.
- Desenvolver um sistema de classificação de risco epidemiológico para as áreas monitoradas.
- Avaliar a viabilidade da utilização da solução por órgãos públicos de vigilância e controle de endemias.
---

# Público-Alvo

## Clientes Potenciais

- Centros de Controle de Zoonoses.
- Secretarias Municipais de Saúde.
- Prefeituras.
- Empresas de monitoramento ambiental.
- Instituições de pesquisa.

---

# Questões de Pesquisa

## Visão Computacional

- Quais objetos possuem maior correlação com focos de dengue?
- Qual modelo apresenta melhor desempenho em imagens de drone?
- Qual resolução mínima é necessária para a detecção confiável?

## Geoprocessamento

- Como converter detecções em coordenadas geográficas?
- Como construir mapas de calor epidemiológicos?

## Engenharia de Software

- Qual arquitetura é mais adequada para escalabilidade?
- Como disponibilizar os resultados para agentes de campo?

---

# Levantamento Bibliográfico

## Temas

### Dengue

- Ciclo do Aedes aegypti.
- Métodos de controle epidemiológico.
- Estratégias de vigilância ambiental.

### Visão Computacional

- Object Detection.
- Segmentação de imagens.
- Redes neurais convolucionais.

### Deep Learning

- YOLO.
- Faster R-CNN.
- RetinaNet.
- RT-DETR.

### Geoprocessamento

- SIG.
- Georreferenciamento.
- PostGIS.
- Mapas de calor.

---

# Tecnologias a Pesquisar

## Inteligência Artificial

- Python
- PyTorch
- TensorFlow
- Ultralytics YOLO

## Visão Computacional

- OpenCV
- Albumentations

## Backend

- FastAPI

## Frontend

- React

## Banco de Dados

- PostgreSQL
- PostGIS

## DevOps

- Docker
- Docker Compose
- GitHub Actions

---
# Database Schema

![Horus DER](docs/diagrams/horus_der.png)
---

# Estrutura Inicial da Solução

## Etapa 1 - Aquisição de Dados

Drone
↓
Captura de imagens
↓
Armazenamento

---

## Etapa 2 - Preparação do Dataset

Imagens
↓
Anotação
↓
Dataset YOLO

Ferramentas avaliadas:

- CVAT
- Label Studio

---

## Etapa 3 - Treinamento

Dataset
↓
YOLO
↓
Modelo treinado

Classes iniciais:

- Poça de água
- Pneu
- Entulho
- Recipiente aberto
- Caixa d'água aberta

---

## Etapa 4 - Inferência

Imagem
↓
Modelo
↓
Detecções

Saída:

- Tipo do objeto
- Confiança
- Coordenadas

---

## Etapa 5 - Plataforma Web

Usuário
↓
Upload de imagens
↓
Processamento
↓
Mapa
↓
Relatório

---

# Métricas de Avaliação

## Modelo de IA

- Precision
- Recall
- F1 Score
- mAP@50
- mAP@50-95

## Sistema

- Tempo de processamento
- Tempo de resposta
- Quantidade de imagens processadas

---

# Viabilidade Comercial

## Proposta de Valor

Reduzir o tempo necessário para localizar possíveis criadouros da dengue por meio da análise automatizada de imagens aéreas.

## Benefícios

- Menor custo operacional.
- Melhor direcionamento das equipes.
- Cobertura mais ampla do território.
- Histórico de monitoramento.

---

# Cronograma Inicial

## Fase 1 — Pesquisa

- Levantamento bibliográfico.
- Estudo dos artigos.
- Definição da arquitetura.

## Fase 2 — Dados

- Organização das imagens.
- Criação do dataset.
- Processo de anotação.

## Fase 3 — IA

- Treinamento inicial.
- Testes.
- Ajustes.

## Fase 4 — Backend

- API de inferência.
- Integração com banco de dados.

## Fase 5 — Frontend

- Dashboard.
- Upload de imagens.
- Visualização dos resultados.

## Fase 6 — Validação

- Testes em imagens reais.
- Comparação com inspeções manuais.

---

# Possíveis Evoluções Futuras

- Aplicativo móvel para agentes.
- Processamento de vídeos.
- Geração automática de rotas de inspeção.
- Monitoramento temporal.
- Previsão de áreas críticas.
- Integração com dados meteorológicos.
- Integração com sistemas municipais.

## Licenciamento

O projeto Horus encontra-se em desenvolvimento no âmbito de pesquisa aplicada e inovação tecnológica.

Todos os direitos são reservados aos autores.

O código-fonte é disponibilizado apenas para fins de pesquisa, avaliação acadêmica e demonstração tecnológica.

Licenciamento comercial futuro poderá ser disponibilizado mediante autorização dos autores.
