# README — Planejamento do Álvaro — Web e Aplicativo Desktop

## Objetivo

Este documento define o planejamento de 15 dias do Álvaro dentro do projeto Horus.

A responsabilidade principal do Álvaro é desenvolver as interfaces que utilizarão o backend desenvolvido pelo Henry:

- Aplicação Web;
- Aplicativo Desktop;
- integração com a API;
- visualização de missões;
- visualização de imagens;
- visualização de detecções;
- visualização das áreas de risco;
- relatórios e informações da missão.

As tecnologias definidas são:

- React;
- Vite;
- JavaScript;
- Electron.

O projeto Web e o Desktop deverão utilizar a mesma lógica de interface sempre que possível, evitando desenvolver duas aplicações completamente diferentes.

---

# Tecnologias

## Web

```text
React
Vite
JavaScript
```

## Desktop

```text
Electron
React
Vite
```

## Comunicação

```text
HTTP
REST API
JSON
```

O backend será desenvolvido pelo Henry utilizando FastAPI.

---

# Estrutura inicial

A aplicação Web já possui uma estrutura inicial com React + Vite.

A organização pode evoluir para:

```text
apps/
├── web/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── utils/
│   └── ...
│
└── desktop/
    ├── electron/
    ├── src/
    └── ...
```

A ideia é manter a maior quantidade possível de código reutilizável entre Web e Desktop.

---

# Relação com o trabalho do Henry

O Álvaro não precisa esperar a API ficar pronta para começar.

Nos primeiros dias, ele pode trabalhar utilizando:

- dados mockados;
- JSON;
- respostas simuladas;
- componentes independentes.

Quando o backend começar a disponibilizar endpoints reais, os mocks deverão ser substituídos pelas chamadas à API.

O objetivo é:

```text
Interface
    ↓
Service/API
    ↓
FastAPI
    ↓
PostgreSQL
```

---

# Plano de 15 dias

## Dia 1 — Conhecer o projeto e definir a interface

Estudar:

- objetivo do Horus;
- fluxo de uma missão;
- informações retornadas pela IA;
- estrutura do banco;
- endpoints que serão necessários;
- informações de uma imagem;
- informações de uma detecção;
- informações de uma área de risco.

Definir as principais telas.

Sugestão inicial:

```text
Login
Dashboard
Missões
Detalhes da missão
Imagens
Detecções
Mapa
Áreas de risco
Relatórios
Configurações
```

### Entrega

Criar uma estrutura inicial das páginas e componentes.

---

# Dia 2 — Estruturar o React

Organizar o projeto React + Vite.

Criar:

```text
src/
├── components/
├── pages/
├── services/
├── hooks/
├── utils/
└── layouts/
```

Criar o sistema básico de navegação.

Exemplo:

```text
/login
/dashboard
/missions
/missions/:id
/reports
/settings
```

### Entrega

Aplicação React organizada e navegável.

---

# Dia 3 — Criar o layout principal

Criar o layout que será utilizado pelo sistema.

Implementar:

- sidebar;
- header;
- navegação;
- conteúdo principal;
- responsividade;
- estados de carregamento;
- mensagens de erro.

A interface deve ser pensada para um usuário que precisa analisar rapidamente os resultados de uma missão.

### Entrega

Layout principal funcional.

---

# Dia 4 — Dashboard

Criar o dashboard inicial.

Mostrar informações como:

```text
Missões realizadas
Imagens processadas
Detecções
Áreas de risco
Últimas missões
```

Inicialmente os dados podem ser mockados.

Exemplo:

```text
Missões: 12
Imagens: 1.428
Detecções: 238
Áreas de risco: 31
```

Os valores reais serão conectados posteriormente à API.

### Entrega

Dashboard visualmente funcional.

---

# Dia 5 — Tela de missões

Criar a página de missões.

Mostrar:

```text
Missão
Data
Status
Piloto
Altitude
Quantidade de imagens
```

Criar:

- listagem;
- busca;
- filtros;
- visualização de detalhes.

### Entrega

Usuário consegue visualizar e selecionar uma missão.

---

# Dia 6 — Tela de detalhes da missão

Criar a página:

```text
/missions/:id
```

Mostrar:

```text
Informações da missão
       ↓
Imagens
       ↓
Detecções
       ↓
Áreas de risco
       ↓
Mapa
```

Inicialmente utilizando dados simulados.

### Entrega

Uma missão pode ser aberta e analisada em uma única página.

---

# Dia 7 — Upload de imagens

Criar a interface para envio das imagens.

Fluxo:

```text
Selecionar missão
       ↓
Selecionar imagens
       ↓
Upload
       ↓
Processamento
       ↓
Resultado
```

Implementar:

- seleção de arquivos;
- múltiplos arquivos;
- barra de progresso;
- estados de carregamento;
- mensagens de erro.

Neste momento o endpoint real do Henry pode ainda não existir.

Usar mocks quando necessário.

### Entrega

Interface de upload funcional.

---

# Dia 8 — Integração inicial com a API

Neste ponto o backend do Henry já deverá estar começando a disponibilizar endpoints.

Criar uma camada central para comunicação:

```text
services/
└── api.js
```

ou equivalente.

Centralizar:

- URL da API;
- autenticação;
- headers;
- tratamento de erros;
- requisições.

Exemplo conceitual:

```javascript
api.get("/missions")
api.get("/missions/1")
api.post("/images")
api.post("/images/1/process")
```

Evitar espalhar chamadas HTTP diretamente pelos componentes.

### Entrega

React conectado aos primeiros endpoints reais.

---

# Dia 9 — Visualização das detecções

Criar interface para apresentar o resultado da IA.

Uma detecção deverá mostrar:

```text
Classe
Confiança
Imagem
Bounding box
Localização
```

Exemplo:

```text
Water Tank
Confidence: 91%
```

Na imagem, desenhar a bounding box correspondente.

Fluxo:

```text
Imagem
   ↓
Detecção
   ↓
Bounding Box
   ↓
Classe + Confiança
```

### Entrega

Usuário consegue visualizar o que a IA detectou.

---

# Dia 10 — Mapa

Criar a visualização geográfica.

Utilizar uma biblioteca adequada para mapas no React.

O mapa deverá mostrar:

```text
Missão
 ↓
Imagens
 ↓
Detecções
 ↓
Áreas de risco
```

Cada área poderá possuir:

```text
latitude
longitude
risk_score
```

Criar diferentes níveis visuais para representar o risco.

### Entrega

Mapa funcional mostrando as informações georreferenciadas retornadas pela API.

---

# Dia 11 — Área de risco

Criar uma interface específica para os resultados de risco.

Mostrar:

```text
Área
Risk Score
Localização
Quantidade de detecções
Principais classes detectadas
```

Exemplo:

```text
Área de risco #12

Score: 82

Detecções:
- 4 pneus
- 2 recipientes
- 1 caixa d'água

Latitude: ...
Longitude: ...
```

Também permitir selecionar a área e visualizar suas imagens relacionadas.

### Entrega

Usuário consegue identificar rapidamente quais regiões precisam de maior atenção.

---

# Dia 12 — Aplicativo Desktop com Electron

Iniciar a aplicação Desktop.

Estrutura básica:

```text
desktop/
├── electron/
│   └── main.js
│
└── src/
```

Configurar:

- Electron;
- janela principal;
- integração com React;
- desenvolvimento local;
- build inicial.

O aplicativo Desktop deverá utilizar a mesma API do sistema.

Arquitetura:

```text
Electron
   ↓
React
   ↓
API
   ↓
FastAPI
```

### Entrega

Aplicativo Electron abre a aplicação React corretamente.

---

# Dia 13 — Adaptar Web + Desktop

Garantir que a interface funcione nos dois ambientes.

Testar:

```text
Web
 ↓
React
 ↓
API
```

e:

```text
Desktop
 ↓
Electron
 ↓
React
 ↓
API
```

Corrigir diferenças relacionadas ao ambiente Desktop.

Evitar colocar lógica específica do Electron dentro dos componentes React quando ela não for necessária.

### Entrega

A mesma aplicação consegue funcionar na Web e no Electron.

---

# Dia 14 — Integração completa

Realizar a integração com o backend.

Testar o fluxo:

```text
Criar/selecionar missão
        ↓
Enviar imagens
        ↓
Processamento
        ↓
IA
        ↓
Detecções
        ↓
Localização
        ↓
Áreas de risco
        ↓
Mapa
```

Testar também:

- erros da API;
- API indisponível;
- imagem inválida;
- upload interrompido;
- ausência de detecções;
- missão sem imagens;
- missão sem áreas de risco.

### Entrega

Web e Desktop funcionando com dados reais do backend.

---

# Dia 15 — Consolidar o MVP

Finalizar a interface.

Revisar:

- navegação;
- responsividade;
- carregamento;
- mensagens de erro;
- integração com API;
- mapas;
- detecções;
- imagens;
- áreas de risco;
- Electron;
- build.

Realizar teste completo.

Criar uma versão funcional:

```text
Horus MVP v1.0
```

---

# Fluxo da aplicação

O usuário deverá conseguir utilizar o sistema aproximadamente assim:

```text
Entrar
  ↓
Dashboard
  ↓
Selecionar missão
  ↓
Visualizar imagens
  ↓
Processar imagens
  ↓
Visualizar detecções
  ↓
Visualizar localização
  ↓
Visualizar áreas de risco
  ↓
Abrir imagens relacionadas
  ↓
Consultar relatório
```

---

# Integração com o backend

O Álvaro deverá consumir os endpoints fornecidos pelo Henry.

Exemplos esperados:

```text
GET  /missions
GET  /missions/{id}

POST /missions

POST /images
GET  /images/{id}

POST /images/{id}/process

GET /missions/{id}/detections

GET /missions/{id}/risk-areas

GET /reports/{id}
```

Os endpoints definitivos serão definidos conforme o backend evoluir.

---

# Dados esperados

Uma missão poderá retornar informações semelhantes a:

```json
{
  "id": 1,
  "name": "Monitoramento Bairro X",
  "date": "2026-08-10",
  "pilot": "Piloto",
  "altitude": 30,
  "status": "processed"
}
```

Uma detecção:

```json
{
  "id": 42,
  "image_id": 15,
  "class": "water_tank",
  "confidence": 0.91,
  "bbox": {
    "x": 0.75,
    "y": 0.33,
    "width": 0.16,
    "height": 0.13
  }
}
```

Uma área de risco:

```json
{
  "id": 10,
  "mission_id": 1,
  "latitude": -20.78,
  "longitude": -51.70,
  "risk_score": 82
}
```

Os formatos acima são exemplos. O contrato definitivo será definido pela API.

---

# Organização do código

Sempre que possível:

```text
Componentes
    ↓
Hooks
    ↓
Services
    ↓
API
```

Evitar:

```text
Componente
   ↓
fetch()
   ↓
URL escrita diretamente
```

Preferir:

```text
Componente
   ↓
Service
   ↓
API
```

Isso facilitará a manutenção e permitirá que Web e Desktop compartilhem a mesma lógica.

---

# Trabalho paralelo com Henry

O desenvolvimento não deve ficar bloqueado enquanto a API não estiver pronta.

Enquanto Henry estiver desenvolvendo:

```text
YOLO
PostgreSQL
FastAPI
```

Álvaro pode utilizar:

```text
mock/
├── missions.json
├── images.json
├── detections.json
└── risk-areas.json
```

Quando os endpoints reais estiverem disponíveis:

```text
MOCK
 ↓
API REAL
```

A interface deverá continuar funcionando sem necessidade de reescrever os componentes.

---

# Trabalho paralelo com Olavo

As informações produzidas pelo Olavo sobre:

- altitude;
- localização;
- drone;
- câmera;
- imagens;
- missão;
- metadados;

deverão ser utilizadas para construir as telas de missão e imagem.

Assim, o sistema poderá apresentar informações como:

```text
Missão
├── Drone
├── Piloto
├── Data
├── Altitude
├── Área monitorada
└── Imagens
      ├── Latitude
      ├── Longitude
      ├── Altitude
      └── Horário
```

---

# Resultado esperado ao final dos 15 dias

Ao final do planejamento, o Álvaro deverá entregar:

```text
Horus Web
    ↓
React + Vite
```

e:

```text
Horus Desktop
    ↓
Electron
    ↓
React
```

Ambos conectados ao mesmo backend.

O usuário deverá conseguir:

- visualizar missões;
- consultar imagens;
- enviar imagens;
- acompanhar processamento;
- visualizar detecções;
- visualizar bounding boxes;
- consultar confiança da IA;
- visualizar coordenadas;
- visualizar áreas de risco;
- visualizar o mapa;
- consultar resultados da missão.

---

# Regra principal

O Álvaro deve priorizar **funcionalidade e integração**, e não tentar construir uma interface gigantesca durante os 15 dias.

O objetivo do MVP é:

> **Permitir que um usuário envie/consulte uma missão e consiga visualizar, de forma clara, o resultado produzido pela IA e pelo backend.**

A aplicação Web e o aplicativo Electron devem funcionar como diferentes interfaces para o mesmo sistema, utilizando a mesma API e, sempre que possível, compartilhando componentes e lógica.
