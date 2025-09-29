# Plano arquitetural — *tech-challenge-01* (Python / GitHub / Heroku)

Abaixo segue um documento detalhado (em português) que descreve a arquitetura proposta para o projeto que você descreveu (scraper → SQLite → Flask APIs → consumo / ML). Usei o repositório informado como referência para a estrutura (src/scripts/scrapping.py e src/api/swt.py). ([GitHub][1])

---

# 1 — Visão geral / Objetivos

* Objetivo 1: *Ingestão* — script (`src/scripts/scrapping.py`) faz scraping em [https://books.toscrape.com/](https://books.toscrape.com/) e popula uma base local (atualmente SQLite). 
* Objetivo 2: *Servir dados* — conjunto de APIs em Flask (`src/api/swt.py`) expõem os dados para consumo por aplicações e por workflows de ciência de dados / ML. As rotas estão protegidas com *JWT Authentication*). 
* Deploy alvo: Heroku (planejado).

---

# 2 — Pipeline (diagrama textual)

```
[books.toscrape.com] 
      ↓ (HTTP scraping)
[Scraping script (scrapping.py) - container / job on scheduler]
      ↓ (normalized records)
[ETL layer] → [Raw staging table(s)] → [Transformations / cleaning]
      ↓
[Primary database (SQLite)]
      ↓
[Flask API service (app.py) — REST endpoints, auth]
      ↓
[Consumers]
  - Data scientists (Jupyter / notebooks / batch training)
  - ML model serving (online / batch)
  - Dashboards / front-end
```

---

# 3 — Observações importantes sobre tecnologias atuais e recomendações

### 3.1 SQLite 

* SQLite é ótimo para prototipação e armazenamento local; **mas não foi pensada para alta concorrência/produção**: suporta muitos leitores simultâneos, porém apenas **um escritor** — o que causa filas/bloqueios em cenários com múltiplos processos/instâncias escrevendo. Para produção ou deploy em Heroku (múltiplos dynos), ao buscar alta disponibilidade **sugestão migrar para PostgreSQL** gerenciado (Heroku Postgres ou similar). 

### 3.2 Autenticação (JWT)

* *JWT* (JSON Web Token) é padrão moderno e amplamente suportado por frameworks, bibliotecas e infra. Essa implementação protege as rotas e garante segurança no acesso aos dados e processos disponibilizados.

### 3.3 Tarefas em background / agendamento

* Para scraping periódico, transformações ou jobs de ingestão em produção, use um worker/queue (ex.: **Celery + Redis** ou **RQ + Redis**) em vez de rodar via cron direto no dyno do web. Isso permite escalonar, retry e observabilidade. 

### 3.4 Model serving / ML

* Para servir modelos em produção recomendo uma camada separada (ex.: MLflow Serving, FastAPI service, or dedicated model server). MLflow oferece features de deploy/serving e versionamento de modelos. 

---

# 4 — Arquitetura proposta (camadas e componentes)

## 4.1 Camada de Ingestão (Scraper)

* **Componente**: `scrapping.py` como tarefa idempotente que:

  * Faz requests .
  * Normaliza dados (title, price, stock, rating, category, url, scraped_at).
  * Registra logs e métricas (tempo, sucesso/falha, contagem).
* **Execução**: como *one-off* local para dev; em produção, rodar como job agendado:

  * Opções: Heroku Scheduler / container cron / CI job / Airflow lightweight / GitHub Actions (para tarefas pouco frequentes).
* **Persistência de ingestão**: grava inicialmente em staging table; transformar e deduplicar antes de inserir no primary DB.

## 4.2 Camada de Armazenamento (DB)

* **Dev / PoC**: SQLite local 
* **Produção / Deploy Heroku**: **migrar para PostgreSQL** (Heroku Postgres) — melhora concorrência, backups, tuning e segurança. (Além disso facilita escalar múltiplos web dynos). 


## 4.3 Camada de API (Flask)

* **Serviço**: `src/api/app.py` — converter para blueprint modular se ainda não estiver, separar responsabilidades (auth, books, admin).
* **Endpoints essenciais** (REST):

  * `GET /books` — list/paginate/filter (category, price range, rating)
  * `GET /books/{id}` — book detail
  * `POST /books/refresh` — trigger ingest (protegido)
  * `GET /meta/stats` — counts, last_scrape, etc.
  * `POST /ml/predict` — (se servir modelo via API)

## 4.4 Camada de ML (integração)

* **Armazenamento features / dataset**:

  * Criar script / endpoint para extrair dataset tabular direto do DB para treino.
  * Versionar datasets (store run id, sample seed).
* **Treino**:

  * Notebooks / pipelines que acessam DB (via read-replica ou export em CSV).
  * Recomendação: rodar treino em ambiente separado (local / cloud), registrar artifacts (model file, metrics) em model registry (MLflow).
* **Serving**:
---

# 5 — Escalabilidade e alta disponibilidade (plano)

1. **DB**: migrar para PostgreSQL gerenciado (Heroku Postgres). Evita problema de locks do SQLite e oferece backups/replicas. 
2. **Web/API**: containerizar (Docker) e rodar múltiplas réplicas (Heroku dynos ou Kubernetes). 
3. **Model Serving**: escalonar modelo separadamente (replicável) — horizontally scale model server. 
4. **Observability**: logs centralizados (Papertrail / LogDNA / Heroku logs), métricas (Prometheus + Grafana / Heroku metrics) e tracing (OpenTelemetry).
