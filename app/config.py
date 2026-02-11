from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "ai-task-agent"
    env: str = "dev"

    # LLM (Ollama local)
    llm_provider: str = "ollama"
    ollama_model: str = "llama3.1:8b"
    ollama_url: str = "http://host.docker.internal:11434/api/chat"

    # Redis/Postgres
    redis_url: str = "redis://localhost:6379/0"
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/agentdb"

    # Agent
    agent_max_steps: int = 6
    tool_timeout_seconds: int = 10

    class Config:
        env_file = ".env"

settings = Settings()
