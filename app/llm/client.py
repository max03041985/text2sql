import httpx
import json
from app.config import settings
from app.llm.prompt import SYSTEM_PROMPT

async def generate_sql(nl_query: str) -> dict:
    payload = {
        "model": settings.LLM_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": nl_query}
        ],
        "format": "json",
        "stream": False,
        "temperature": 0.1
    }
    
    async with httpx.AsyncClient(timeout=settings.LLM_TIMEOUT) as client:
        response = await client.post(settings.OLLAMA_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
    try:
        content = result["message"]["content"]
        return json.loads(content)
    except (json.JSONDecodeError, KeyError) as e:
        raise RuntimeError(f"Failed to parse LLM JSON response: {e}")