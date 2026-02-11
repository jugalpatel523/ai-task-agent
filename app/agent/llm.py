import json
import httpx
from app.config import settings
from app.utils.retry import with_retry

class LLMClient:
    """
    100% free local LLM via Ollama.
    """

    def __init__(self):
        if settings.llm_provider != "ollama":
            raise ValueError("This project template is set up for ollama provider.")
        self.model = settings.ollama_model
        self.url = settings.ollama_url

    @with_retry(3)
    async def chat_json(self, system: str, messages: list[dict]) -> dict:
        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": system}] + messages,
            "stream": False,
            # Request JSON-only responses (Ollama will try to comply)
            "format": "json"
        }

        async with httpx.AsyncClient(timeout=90) as client:
            r = await client.post(self.url, json=payload)
            r.raise_for_status()
            data = r.json()

        # Ollama returns JSON content as a string in message.content
        content = data["message"]["content"]
        return json.loads(content)
