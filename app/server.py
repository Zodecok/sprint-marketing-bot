from fastapi import FastAPI
from app.settings import settings

app = FastAPI(title="Sprint Marketing Bot API")

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": settings.ollama_model,
        "embeddings": settings.embeddings_model
    }
