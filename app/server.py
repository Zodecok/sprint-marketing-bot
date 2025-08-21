from fastapi import FastAPI, HTTPException
from app.settings import settings
from app.models import ChatRequest, ChatResponse, Source
from app.rag_pipeline import retrieve, build_prompt
from app.deps.llm import complete

app = FastAPI(title="Sprint Marketing Bot API")

@app.get("/health")
def health():
    return {"status": "ok", "model": settings.ollama_model, "embeddings": settings.embeddings_model}

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        hits = retrieve(req.query, settings.top_k)
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="No index found. Run ingest first.")

    contexts = [h[1] for h in hits]
    prompt = build_prompt(req.query, contexts)
    answer = await complete(prompt)

    sources = [
        Source(
            doc_path=h[1]["doc_path"],
            chunk_id=h[1]["chunk_id"],
            score=h[0],
            preview=h[1]["chunk"][:240]
        )
        for h in hits
    ]
    return ChatResponse(answer=answer, sources=sources)
