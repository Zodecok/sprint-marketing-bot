from fastapi import FastAPI, HTTPException
from uuid import uuid4
from app.settings import settings
from app.models import ChatRequest, ChatResponse
from app.rag_pipeline import retrieve, build_prompt
from app.deps.llm import complete
from app.utils.logger import log_chat
from app.utils.index_manifest import read_index_manifest
import logging

# Set up logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sprint Marketing Bot API")
_manifest = read_index_manifest()

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": settings.ollama_model,
        "embeddings": settings.embeddings_model,
        "index_version": _manifest.get("index_version"),
        "chunks": _manifest.get("chunks_count"),
    }

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
    
    request_id = str(uuid4())
    index_version = _manifest.get("index_version", "unknown")

    try:
        hits = retrieve(req.query, settings.top_k)
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="No index found. Run ingest first.")

    if not hits:
        answer = "I don’t have that information in my sources yet."
        log_chat(
            request_id=request_id,
            index_version=index_version,
            query=req.query,
            answer=answer,
            hits=[],
            config={
                "top_k": settings.top_k,
                "retrieval_candidates": settings.retrieval_candidates,
                "min_sim": settings.min_sim,
                "enable_rerank": settings.enable_rerank,
                "reranker_model": settings.reranker_model,
            },
        )
        return ChatResponse(answer=answer, has_sources=False, source_count=0, request_id=request_id)
    
    # build prompt and answer
    contexts = [h[1] for h in hits]
    prompt = build_prompt(req.query, contexts)
    answer = await complete(prompt)

    # Log full provenance server-side only
    log_chat(
        request_id=request_id,
        index_version=index_version,
        query=req.query,
        answer=answer,
        hits=hits,
        config={
            "top_k": settings.top_k,
            "retrieval_candidates": settings.retrieval_candidates,
            "min_sim": settings.min_sim,
            "enable_rerank": settings.enable_rerank,
            "reranker_model": settings.reranker_model,
        },
    )
    
    return ChatResponse(answer=answer, has_sources=True, source_count=len(hits), request_id=request_id,)