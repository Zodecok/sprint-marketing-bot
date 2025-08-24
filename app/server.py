from fastapi import FastAPI, HTTPException
from app.settings import settings
from app.models import ChatRequest, ChatResponse, Source
from app.rag_pipeline import retrieve, build_prompt
from app.deps.llm import complete
from app.deps.logger import log_chat

app = FastAPI(title="Sprint Marketing Bot API")

@app.get("/health")
def health():
    return {"status": "ok", "model": settings.ollama_model, "embeddings": settings.embeddings_model}

def _bad_query(q:str) -> bool:
    # Hard limits
    if not q or len(q) > settings.bad_query_length:
        return True
    # Very simple prompt-injection heuristics (PI [Prompt Injection])
    lowered = q.lower()
    red_flags = [
        "ignore previous instructions",
        "act as system",
        "you are now",
        "override",
        "developer mode",
    ]
    return any(flag in lowered for flag in red_flags)

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if _bad_query(req.query):
        raise HTTPException(status_code=400, detail="Invalid or disallowed query.")
    
    try:
        hits = retrieve(req.query, settings.top_k)
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="No index found. Run ingest first.")

    if not hits:
        answer = "I don’t have that information in my sources yet."
        log_chat(req.query, answer, [])
        return ChatResponse(answer=answer, sources=[])
    
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
    log_chat(req.query, answer, hits)
    return ChatResponse(answer=answer, sources=sources)
