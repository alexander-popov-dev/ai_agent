# AI Reels Creator

An AI-powered Telegram bot that walks a user through a full **Reels content pipeline**: pick a pipeline → choose a niche → pick a language → generate ideas → select an idea (or regenerate with instructions) → generate a story → review an AI critique → edit or approve.

The conversational flow is built on **LangGraph** with human-in-the-loop interrupts, state persisted in a **PostgreSQL** checkpointer, session state in **Redis**, and LLM providers (OpenRouter, Google, Ollama, Groq, Mistral) selected per pipeline step.

---

## Table of contents

- [Stack](#stack)
- [Architecture](#architecture)
- [Project structure](#project-structure)
- [LangGraph workflow](#langgraph-workflow)
- [Getting started](#getting-started)
- [.env reference](#env-reference)
- [Database migrations](#database-migrations)
- [Running the bot](#running-the-bot)
- [Makefile & Docker](#makefile--docker)
- [AI providers configuration](#ai-providers-configuration)
- [Logging](#logging)
- [Troubleshooting](#troubleshooting)

---

## Stack

| Layer | Technology |
|---|---|
| Language / runtime | Python 3.13, managed with [uv](https://docs.astral.sh/uv/) |
| Bot framework | [aiogram](https://docs.aiogram.dev/) 3.x |
| Orchestration | [LangGraph](https://langchain-ai.github.io/langgraph/) + `langgraph-checkpoint-postgres` |
| LLM tooling | langchain, langchain-openrouter, langchain-google-genai, langchain-ollama, langchain-groq, langchain-mistralai |
| DI | [dishka](https://dishka.readthedocs.io/) (async container, aiogram integration) |
| Relational DB | PostgreSQL via SQLAlchemy 2 (async) + asyncpg; psycopg3 pool for the LangGraph checkpointer |
| FSM / chat state | Redis (`aiogram.fsm.storage.redis.RedisStorage`) |
| Migrations | Alembic (async engine) |
| Config | pydantic-settings (`.env` + `.env.local`) |
| Logging | structlog (console or JSON) |

---

## Architecture

The codebase is layered — Telegram handlers never talk to the DB or LLMs directly:

```
src/
├── telegram/      # aiogram routers, keyboards, callbacks, FSM contexts  (delivery layer)
├── application/   # services + repositories + SQLAlchemy models          (domain layer)
├── pipelines/     # LangGraph workflows, agents, prompt schemas          (workflow layer)
├── ai/            # providers registry, agent factory, prompt factory    (LLM layer)
├── database/      # engines, DI providers, alembic migrations, redis     (infra layer)
└── core/          # container, settings, enums, logging                  (shared kernel)
```

### Dependency injection

`src/core/container.py` builds a single async **dishka** container from 7 providers:

| Provider | Provides |
|---|---|
| `PostgresProvider` | SQLAlchemy engine, request-scoped `AsyncSession` (commit/rollback), `AsyncPostgresSaver` checkpointer (dedicated `psycopg` pool, `autocommit=True`) |
| `RedisFSMDBProvider` | Redis client for aiogram FSM |
| `TelegramProvider` | `TelegramSettings`, `Bot` (default `parse_mode=HTML`), `RedisStorage`, `Dispatcher` |
| `AIProviderProvider` | AI application services |
| `UserProvider` / `NicheProvider` / `PipelineProvider` | domain services & repositories |
| `ReelsPipelineProvider` | `ReelsPipelineService` (start/resume the graph), with `LoggedMixin` |

Handlers receive dependencies via `@inject` + `FromDishka[...]`; `setup_dishka(...)` wires the container into the dispatcher at startup (`src/main.py`).

### Request flow

```
Telegram update
  → aiogram dispatcher (Redis FSM storage)
  → router/handler (dishka-injected services)
  → ReelsPipelineService.start() / .resume()
  → LangGraph compiled graph (Postgres checkpointer, thread_id = session UUID)
  → interrupt()  ← user decision comes back as Command(resume=...)
  → handler renders the next screen
```

---

## Project structure

```
.
├── alembic.ini                  # alembic config (script_location → src/database/postgres/migration)
├── Makefile                     # docker compose shortcuts
├── pyproject.toml               # dependencies (uv-managed, see uv.lock)
├── deploy/
│   ├── Dockerfile               # python:3.13-slim + uv sync, CMD python -m src.main
│   └── docker-compose.yaml      # tg-bot service (infra services are commented out)
└── src/
    ├── main.py                  # entry point: container → routers → polling
    ├── settings.py              # BaseProjectSettings (reads .env, .env.local)
    ├── ai/
    │   ├── providers/           # BaseProvider + registry: google, openrouter, ollama, groq, mistral
    │   ├── agent/               # BaseAgent + AgentFactory
    │   ├── prompt/              # PromptFactory
    │   └── settings.py          # API keys (SecretStr) from .env
    ├── application/
    │   ├── user/ niche/ pipeline/ ai/   # service + repository + schemas + DI per domain
    ├── core/
    │   ├── container.py         # create_container()
    │   ├── settings.py          # DEBUG / LOG_LEVEL / LOG_JSON
    │   ├── enums.py             # Language (en/ua/ru)
    │   └── logging/             # structlog config, LoggedMixin, decorators
    ├── database/
    │   ├── postgres/            # engine, models (BaseModel), DI, migration/
    │   │   └── migration/versions/   # alembic revisions
    │   ├── redis/               # redis DI (components: default, cache, fsm)
    │   └── qdrant/              # vector store repositories
    ├── pipelines/
    │   ├── core/                # PipelineSessionStatus
    │   └── reels/
    │       ├── idea/            # GenerateIdea agent + schemas
    │       ├── story/           # GenerateStory / EditStory agents + schemas
    │       ├── critic/          # CritiqueStory agent + schemas
    │       ├── workflow/        # graph, nodes, state, decisions, service, contracts
    │       ├── enums.py         # ReelsAgent keys
    │       └── di.py            # ReelsPipelineProvider
    └── telegram/
        ├── di.py                # Bot / Dispatcher / RedisStorage
        ├── settings.py          # TELEGRAM_BOT_TOKEN
        ├── common/              # context helpers, bot commands, error handler
        ├── reels/               # funnel routers: pipeline → niche → language → idea → story
        │   ├── callbacks.py     # ReelsCallback (prefix="reels")
        │   ├── context.py       # ReelsContext / ReelsAction (stored in FSM)
        │   └── state.py         # aiogram StatesGroup
        └── pipeline_settings/   # settings funnel: pipeline, step, provider, model, temperature
            └── callbacks.py     # SettingsCallback (prefix="settings")
```

> **Callback namespaces:** `ReelsCallback` uses prefix `reels`, `SettingsCallback` uses prefix `settings` — this is what keeps the two funnels from colliding.

---

## LangGraph workflow

Implemented in `src/pipelines/reels/workflow/`:

```
START
  │
  ▼
generate_ideas ──────► choose_idea ◄── interrupt #1 (pick an idea / ask for more)
  ▲                       │
  └───── regenerate ──────┤
                          │ choose
                          ▼
                   generate_story
                          │
                          ▼
                   critique_story      (informational — shown to the user, does not rewrite)
                          │
                          ▼
                   review_story ◄────── interrupt #2 (approve / edit)
                     │         │
              approve│         │edit
                     ▼         ▼
                   END     edit_story ──► critique_story (loop)
```

Key points:

- **`ReelsState`** (`workflow/state.py`) is a pydantic model persisted by the checkpointer: `ideas` (current batch), `generated_ideas` (full history used to avoid duplicates), `idea_instructions`, `idea_regenerations`, `story`, `critique`, `story_instructions`, `story_edits`, `is_approved`.
- **Interrupts** are resolved by the Telegram layer: the handler calls `ReelsPipelineService.resume(...)` with a validated `ChooseIdeaDecision` or `ReviewStoryDecision` (`workflow/decisions.py`).
- **User instructions matter**: instructions typed while regenerating ideas accumulate in `idea_instructions`, are passed into `GenerateIdeaInput.instructions`, and are cleared after each successful generation.
- **Limits:** `MAX_IDEA_REGENERATIONS = 5`, `MAX_STORY_EDITS = 5`.
- **Persistence:** each run's `thread_id` is the `UserPipelineSession` UUID; the app-side session row (status/ownership) lives in PostgreSQL alongside the LangGraph checkpoint tables.
- The graph is **built per user session** (`build_reels_graph`) and compiled with the shared APP-scoped `AsyncPostgresSaver`.

---

## Getting started

### Prerequisites

- Python **3.13** (see `.python-version`)
- [uv](https://docs.astral.sh/uv/)
- PostgreSQL 17+ and Redis 8 (local, Docker, or remote)
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- At least one LLM provider API key (OpenRouter, Google, ...)

### 1. Install dependencies

```bash
uv sync
```

(or work inside an existing `.venv` — the project was developed with `.venv\Scripts\python.exe`).

### 2. Configure environment

Create a `.env` file in the repo root (see [.env reference](#env-reference)). All secrets live **only** here — never in the database; pydantic-settings loads `.env` and `.env.local` (overrides).

### 3. Start infrastructure

PostgreSQL and Redis must be reachable at the configured `PG_*` / `REDIS_*` addresses. If you use the commented-out services in `deploy/docker-compose.yaml`, uncomment them and run:

```bash
make up-db     # docker compose -f deploy/docker-compose.yaml --env-file .env up -d
```

### 4. Run migrations

```bash
alembic upgrade head
```

### 5. Start the bot

From the repository root:

```bash
python -m src.main
```

> **Windows note:** the entry point must set `asyncio.WindowsSelectorEventLoopPolicy` before starting (required by psycopg/redis on the Windows selector loop). Make sure that block in `src/main.py` is enabled when you run on Windows.

---

## .env reference

All variables read by the app (names only — fill in your own values):

| Variable | Required | Description |
|---|---|---|
| `DEBUG` | ✅ | Enables debug rendering (e.g. colored structlog console) |
| `LOG_LEVEL` | ✅ | Logging level (`INFO`, `DEBUG`, ...) |
| `LOG_JSON` | ⬜ | `true` → JSON logs (recommended in Docker) |
| `COMPOSE_PROJECT_NAME` | ⬜ | Docker compose project name |
| `PG_HOST` | ✅ | PostgreSQL host |
| `PG_PORT` | ✅ | PostgreSQL port (server side) |
| `PG_PORT_LOCAL` | ⬜ | Host port mapped to 5432 (compose) |
| `PG_NAME` | ✅ | Database name |
| `PG_USER` | ✅ | Database user |
| `PG_PASS` | ✅ | Database password |
| `REDIS_HOST` | ✅ | Redis host |
| `REDIS_PORT` | ✅ | Redis port (server side) |
| `REDIS_PORT_LOCAL` | ⬜ | Host port mapped to 6379 (compose) |
| `REDIS_PASS` | ✅ | Redis password |
| `QDRANT_HOST` | ⬜ | Qdrant host (vector store, optional for current flows) |
| `QDRANT_PORT` | ⬜ | Qdrant port |
| `N8N_HOST` / `N8N_PORT` | ⬜ | n8n (compose automation stack, not required by the bot) |
| `TZ` | ⬜ | Timezone for the compose stack |
| `TELEGRAM_BOT_TOKEN` | ✅ | Token from @BotFather |
| `OPENROUTER_API_KEY` | ⬜* | OpenRouter API key |
| `GOOGLE_API_KEY` | ⬜* | Google Gemini API key |
| `MISTRAL_API_KEY` | ⬜* | Mistral API key |
| `GROQ_API_KEY` | ⬜* | Groq API key |
| `OPENROUTER_BASE_URL` | ⬜ | Defaults to `https://openrouter.ai/api/v1` |
| `OLLAMA_BASE_URL` | ⬜ | Defaults to `http://localhost:11434` |

\* provide keys for whichever providers you actually enable in the bot settings.

API keys are exposed to the code as `SecretStr` (`src/ai/settings.py`) and must never be stored in the database.

---

## Database migrations

- Config: `alembic.ini` → `script_location = src/database/postgres/migration`
- The DB URL is injected by `migration/env.py` from `get_database_settings()` (i.e. from `.env`), **not** from `alembic.ini`.
- Models metadata: `src/database/postgres/model.py::BaseModel` (autogenerate supported).

```bash
alembic upgrade head                       # apply
alembic revision --autogenerate -m "..."   # create a new revision
```

LangGraph checkpoint tables are created automatically at startup by `AsyncPostgresSaver.setup()` — no alembic revision needed for them.

---

## Running the bot

```bash
python -m src.main
```

Startup sequence (`src/main.py`):

1. `configure_logging()` — structlog from `LOG_LEVEL` / `LOG_JSON`;
2. create the dishka container;
3. resolve `Bot` and `Dispatcher`;
4. include routers: `reels`, `pipeline_settings`, `errors`;
5. `setup_dishka(...)` — inject dependencies into handlers;
6. `set_bot_commands(bot)` — menu commands;
7. `dp.start_polling(bot)`.

Run this **from the repo root** — the same working directory is assumed by the Dockerfile (`WORKDIR /app`, `CMD python -m src.main`).

---

## Makefile & Docker

`Makefile` wraps `docker compose -f deploy/docker-compose.yaml --env-file .env`:

| Target | Effect |
|---|---|
| `make up` / `stop` / `down` / `logs` | App profile: build/run/stop/logs for the `tg-bot` service |
| `make up-db` / `stop-db` / `down-db` / `logs-db` | Full stack (infra) — works only if the infra services are uncommented |
| `make rebuild` | Recreate the stack |

Current state to be aware of:

- **Infra services (postgres, redis, qdrant, n8n, ollama) are commented out** in `deploy/docker-compose.yaml`; only `tg-bot` is active. The compose file expects external networks `internal` and `traefik-public` to already exist on the host.
- The `Makefile` defines a `COMPOSE_MONITORING` variable pointing at `monitoring/docker-compose.yaml`, which is **not present** in the repo — it is unused.

Docker image (`deploy/Dockerfile`):

```dockerfile
FROM python:3.13-slim
# uv sync --frozen --no-dev  → reproducible install from uv.lock
CMD ["python", "-m", "src.main"]
```

`.env` is passed to the container via `env_file: ../.env`.

Typical deploy:

```bash
make up      # build + start the bot container
make logs    # follow logs
```

---

## AI providers configuration

Two configuration planes:

1. **Secrets** — API keys in `.env` only (`src/ai/settings.py`, `SecretStr`).
2. **Selection** — which provider/model/temperature each pipeline step uses is stored **in the database** and managed from the bot itself:

   - settings funnel (`src/telegram/pipeline_settings/`): pipeline → step → provider → model → temperature;
   - registry tables `ai_provider` and `ai_model` (`src/application/ai/models.py`) with `is_active` flags;
   - per-step user settings are resolved into `PipelineStepWithUserSettingsSchema`.

At runtime:

```
AgentFactory.create(pipeline_step)
  ├─ ProviderFactory  → BaseProvider registry (google / openrouter / ollama / groq / mistral)
  ├─ PromptFactory    → prompt for the step
  └─ BaseAgent        → executes with structured pydantic output
```

The four Reels agents are keyed by `ReelsAgent`: `generate_ideas`, `generate_story`, `edit_story`, `critique_story`.

---

## Logging

- `src/core/logging/config.py` configures **structlog** at import time of `main.py`.
- `LOG_LEVEL` sets the level; `LOG_JSON=false` gives a colored console renderer (uses `DEBUG`), `LOG_JSON=true` emits one JSON object per line — recommended in Docker.
- Services inherit `LoggedMixin` for consistent logger names.
- Output goes to **stdout** (`stream=sys.stdout`) so `docker logs` picks it up.

---

## Troubleshooting

**Bot doesn't start on Windows / `proactor` event-loop errors**
The entry point must set `asyncio.WindowsSelectorEventLoopPolicy()` before `asyncio.run(tg())` — required by psycopg and redis on Windows. Check the `if __name__ == '__main__':` block in `src/main.py`.

**`TelegramBadRequest: Unsupported start tag / can't parse entities`**
The bot sends messages with global `parse_mode=HTML`. Any text coming from the LLM (ideas, story, critique, error messages) must be passed through `html.escape()` before sending. If a new screen renders raw model output, this error will appear.

**`TelegramBadRequest: message_ids must be non-empty` / wrong length**
`Bot.delete_messages()` accepts **1–100** ids. Guard empty lists before calling (see `clear_idea_messages` in `src/telegram/reels/idea/handlers.py`).

**Buttons show a loading spinner until timeout (~30s)**
The callback wasn't acknowledged — add `await callback.answer()` at the top of the handler.

**Callback routed to the wrong funnel**
`ReelsCallback` and `SettingsCallback` must keep distinct prefixes (`reels` vs `settings`).

**LangGraph state lost between updates**
Checkpoints live in PostgreSQL via `AsyncPostgresSaver`; the pool is created with `autocommit=True` (`src/database/postgres/di.py`). Ensure the DB is reachable and `checkpointer.setup()` ran.

**FSM state lost**
aiogram FSM uses Redis (`RedisStorage`, component `fsm`). Verify `REDIS_*` settings.

**Provider errors like `provider_overloaded`**
LLM calls are single-shot (`BaseAgent.execute` → `chain.ainvoke`, no automatic retry yet). Check your provider quota/keys in `.env`, the per-step model selection in the bot settings — or add a retry policy (e.g. `tenacity`, already in dependencies) around the chain.
