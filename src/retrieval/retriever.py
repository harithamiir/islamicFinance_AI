"""
retriever.py — Embed a query and find the most relevant chunks in Qdrant.

The returned list of result dicts is passed directly to the generator.
Each result has:
  text        : the chunk text
  score       : cosine similarity (0–1, higher is better)
  source_type : quran | hadith | scholar | aaoifi
  filename    : source file name
  chunk_index : position within the original document
"""

from openai import OpenAI
from qdrant_client import QdrantClient

from config import (
    OPENAI_API_KEY,
    EMBEDDING_MODEL,
    QDRANT_URL,
    QDRANT_HOST,
    QDRANT_PORT,
    QDRANT_API_KEY,
    COLLECTION_NAME,
    TOP_K,
)

_openai = OpenAI(api_key=OPENAI_API_KEY)
if QDRANT_URL:
    _qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
else:
    _qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY)


def retrieve(query: str, top_k: int = TOP_K) -> list[dict]:
    """
    Embed the query and return the top_k most similar chunks.

    Args:
        query  : the user's question
        top_k  : number of results to return (default from config)

    Returns:
        List of result dicts sorted by similarity (best first).
    """
    # Embed the question using the same model used during ingestion
    response = _openai.embeddings.create(model=EMBEDDING_MODEL, input=[query])
    query_vector = response.data[0].embedding

    response = _qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True,
    )

    results = []
    for hit in response.points:
        payload = hit.payload or {}
        results.append({
            "text": payload.get("text", ""),
            "score": round(hit.score, 4),
            "source_type": payload.get("source_type", "unknown"),
            "filename": payload.get("filename", "unknown"),
            "chunk_index": payload.get("chunk_index", 0),
            "surah": payload.get("surah"),   # Quran only, None for other sources
            "ayah": payload.get("ayah"),     # Quran only, None for other sources
        })

    return results
