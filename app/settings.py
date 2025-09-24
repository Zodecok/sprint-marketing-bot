from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    llm_provider: str = os.getenv("LLM_PROVIDER", "ollama")
    
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    
    embeddings_model: str = os.getenv("EMBEDDINGS_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "180"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "30"))
    bad_query_length: int = int(os.getenv("BAD_QUERY_LENGTH", "1000"))

    #retriever settings
    retrieval_candidates: int = int(os.getenv("RETRIEVAL_CANDIDATES", "20"))
    min_sim: float = float(os.getenv("MIN_SIM", "0.25"))
    # Prefer RETRIEVAL_TOP_K; fall back to legacy TOP_K for compatibility
    retrieval_top_k: int = int(os.getenv("RETRIEVAL_TOP_K", os.getenv("TOP_K", "5")))

    #reranker settings
    enable_rerank: str = os.getenv("ENABLE_RERANK", "false")
    reranker_model: str = os.getenv("RERANKER_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")

settings = Settings()
