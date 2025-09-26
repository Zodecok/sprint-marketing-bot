# app/deps/llm.py
from __future__ import annotations
import httpx
from app.settings import settings

# Public, provider-agnostic entrypoint
async def complete(prompt: str) -> str:
    provider = (settings.llm_provider or "ollama").lower()
    if provider == "ollama":
        return await complete_ollama(prompt)
    # Stubs for future providers; raise a clear error for now
    raise ValueError(f"Unsupported LLM_PROVIDER='{settings.llm_provider}'. "
                     f"Supported: ['ollama'] for now.")
    #TODO: add more providers and a proper catch for this error

# Concrete Ollama client
async def complete_ollama(prompt: str) -> str:
    url = f"{settings.ollama_base_url}/api/generate"
    payload = {
        "model": settings.ollama_model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.3}
    }
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(url, json=payload)
        r.raise_for_status()
        data = r.json()
        #TODO: handle streaming responses if needed
    return (data.get("response") or "").strip()
