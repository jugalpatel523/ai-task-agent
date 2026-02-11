# AI Task Agent (Local LLM + Tools + Memory)

Production-style AI task agent built with FastAPI that plans multi-step execution, calls tools, and persists execution history using Postgres and Redis.

This project demonstrates how modern AI agents orchestrate tools, maintain memory, and expose reliable APIs using backend engineering best practices.

---

## 🚀 Features

- Multi-step agent execution with reasoning loop
- Tool calling framework (calculator, text explanation, search, DB lookup)
- Tool registry with schema validation (Pydantic)
- Persistent run history stored in Postgres
- Short-term memory support via Redis
- FastAPI REST APIs with OpenAPI (Swagger)
- Reliability features:
  - retries
  - timeouts
  - idempotent runs (run_id)
- Dockerized local environment

---

## Architecture

The system follows an agentic execution architecture where the LLM plans steps, invokes tools via a registry, and persists execution state for reproducibility and observability.

```mermaid
flowchart TD
  U[Client (Swagger UI / curl)] -->|POST /runs| API[FastAPI API (app/main.py)]

  API --> AR[Agent Runner (Planning + Execution)]

  AR -->|store runs + messages| PG[(Postgres: Runs + Messages)]
  AR -->|short-term memory| REDIS[(Redis: Memory Cache)]

  AR -->|prompt + context| LLM[Local LLM Provider (Ollama + Llama 3.x)]

  LLM -->|tool calls| TR[Tool Registry (app/tools/registry.py)]

  TR --> CALC[Calculator Tool]
  TR --> SEARCH[Text Search Tool]
  TR --> DBL[DB Lookup Tool]
  TR --> TEX[Text Explain Tool]

  CALC --> AR
  SEARCH --> AR
  DBL --> AR
  TEX --> AR

  AR -->|final answer + steps| API
  API -->|GET /runs/{run_id}| U
```

## 🧠 Architecture Overview

Client Request
↓
FastAPI API Layer
↓
Agent Runner
↓
Tool Registry
↓
Tool Execution
↓
Postgres (runs + messages)
↓
Redis (memory/cache)



### Core Components

| Component | Responsibility |
|------------|---------------|
| `agent/runner.py` | Agent execution loop |
| `tools/registry.py` | Tool registration & lookup |
| `tools/.py` | Tool implementations |
| `db.py` | Database session management |
| `models.py` | SQLAlchemy models |
| `schemas.py` | API + tool validation schemas |

---

## 🧰 Implemented Tools

### Calculator
Performs arithmetic operations using structured tool inputs.

Example:
23 * 19 → 437


### Text Explain
Converts numeric or technical output into simple human-readable explanations.

### DB Lookup
Simulates database queries (extensible to real Postgres queries).

### Text Search
Simple search tool stub for extensibility.

---

## 🤖 LLM Provider (Free)

Uses a local open-source LLM via **Ollama (Llama 3.1)**.

- No API costs
- Provider-agnostic architecture
- Can be swapped with OpenAI / Bedrock / Azure OpenAI

---

## ⚡ Quickstart (Docker)

### 1. Install
- Docker Desktop
- Ollama

### 2. Pull model
```bash
ollama pull llama3.1:8b
```

3. Setup environment

cp .env.example .env

(Windows)

copy .env.example .env

4. Run

docker compose up --build

5. Open Swagger

http://localhost:8000/docs

📘 Example

POST /runs

{
  "user_id": "demo",
  "goal": "Use calculator to compute 23*19 and explain the result."
}

Response includes:

reasoning steps

tool calls

observations

final answer


🧱 Tech Stack

Python 3.11

FastAPI

SQLAlchemy

Postgres

Redis

Docker & Docker Compose

Pydantic

Ollama (Local LLM)


🎯 Why This Project

Modern AI systems require more than prompting — they need:

tool orchestration

memory

persistence

reliability

API-driven execution

This project demonstrates how AI agents can be built using production backend engineering patterns.


👤 Author

Jugal Patel
Software Engineer | Backend & AI Systems