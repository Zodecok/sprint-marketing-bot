from sentence_transformers import SentenceTransformer
from functools import lru_cache
from app.settings import settings

@lru_cache(maxsize=1)
def get_embedder():
    return SentenceTransformer(settings.embeddings_model)

def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_embedder()
    return model.encode(texts, convert_to_numpy=True, show_progress_bar=False).tolist()
