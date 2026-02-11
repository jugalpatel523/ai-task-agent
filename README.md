# AI Task Agent (100% Free Local LLM)

Production-style LLM agent that can:
- plan multi-step execution
- call tools (calculator, search stub, db lookup stub)
- store short-term memory in Redis (per user)
- persist runs + messages to Postgres
- expose APIs via FastAPI
- reliability: timeouts, retries, idempotency (run_id)

## LLM Provider (Free)
This repo uses a local open-source LLM (Ollama + Llama 3.1) so running is $0.
Architecture is provider-agnostic and can be swapped to managed APIs later.

## Quickstart (Docker)
1) Install Docker Desktop + Ollama
2) Pull model:
   `ollama pull llama3.1:8b`
3) Copy env:
   `cp .env.example .env` (Windows: `copy .env.example .env`)
4) Run:
   `docker compose up --build`
5) Open Swagger:
   http://localhost:8000/docs

## Example
POST /runs
```json
{
  "user_id": "jugal",
  "goal": "Compute (12^2 + 5) / 7 and explain steps."
}
