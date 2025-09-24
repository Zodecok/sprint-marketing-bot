from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from uuid import uuid4
from app.settings import settings
from app.models import ChatRequest, ChatResponse
from app.rag_pipeline import retrieve, build_prompt
from app.deps.llm import complete
from app.utils.logger import log_chat, _redact
from app.utils.index_manifest import read_index_manifest
import logging
import time
from app.models import UIEventIn, ConversationList, ConversationSummary
from app.utils.paths import ui_events_log_path, conversations_log_path
from app.utils.log_io import jsonl_append, jsonl_tail

# Set up logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sprint Marketing Bot API")

# CORS for local development frontends (adjust as needed)
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    # Allow credentials so browsers accept preflight for dev origin 5173
    # Even though we don't currently use cookies/Authorization, some browsers
    # require this header when the request's credentials mode is 'include'.
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    max_age=86400,
)
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
        hits = retrieve(req.query, settings.retrieval_top_k)
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
                "retrieval_top_k": settings.retrieval_top_k,
                "retrieval_candidates": settings.retrieval_candidates,
                "min_sim": settings.min_sim,
                "enable_rerank": settings.enable_rerank,
                "reranker_model": settings.reranker_model,
            },
        )
        # Minimal conversations summary writer (no sources case)
        jsonl_append(
            conversations_log_path(),
            {
                "ts": int(time.time() * 1000),
                "user": _redact(req.query),
                "assistant": _redact(answer)[:2000],
            },
        )
        return ChatResponse(answer=answer, has_sources=False, source_count=0, request_id=request_id)
    
    # build prompt and answer
    contexts = [h[1] for h in hits]
    prompt = build_prompt(req.query, contexts)
    t0 = time.monotonic()
    answer = await complete(prompt)
    completion_ms = int((time.monotonic() - t0) * 1000)

    # Log full provenance server-side only
    log_chat(
        request_id=request_id,
        index_version=index_version,
        query=req.query,
        answer=answer,
        hits=hits,
        config={
            "retrieval_top_k": settings.retrieval_top_k,
            "retrieval_candidates": settings.retrieval_candidates,
            "min_sim": settings.min_sim,
            "enable_rerank": settings.enable_rerank,
            "reranker_model": settings.reranker_model,
        },
        completion_timetaken_ms=completion_ms,
    )
    # Minimal conversations summary writer (with sources case)
    jsonl_append(
        conversations_log_path(),
        {
            "ts": int(time.time() * 1000),
            "user": _redact(req.query),
            "assistant": _redact(answer)[:2000],
        },
    )

    return ChatResponse(answer=answer, has_sources=True, source_count=len(hits), request_id=request_id,)


@app.post("/ui_event")
def ui_event(evt: UIEventIn):
    record = {
        "ts_server": int(time.time() * 1000),
        "ts_client": evt.ts,
        "name": evt.name,
        "payload": evt.payload or {},
    }
    jsonl_append(ui_events_log_path(), record)
    return {"ok": True}


@app.get("/conversations", response_model=ConversationList)
def conversations(limit: int = Query(50, ge=1, le=500)):
    # Reads from a JSONL file you populate when /chat completes
    raw = jsonl_tail(conversations_log_path(), limit)
    items: List[ConversationSummary] = []
    for r in raw:
        try:
            items.append(ConversationSummary(
                ts=int(r.get("ts", int(time.time() * 1000))),
                user=str(r.get("user", ""))[:300],
                assistant=str(r.get("assistant", ""))[:300],
            ))
        except Exception:
            continue
    # reverse so newest first if your logger appends chronologically
    items = list(reversed(items))
    return ConversationList(items=items)
