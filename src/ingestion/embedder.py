"""
embedder.py — Embed chunks with OpenAI and upload them to Qdrant.

This is the most expensive step (API calls + storage).
Run it once when you add new documents. Re-running is safe —
Qdrant upsert will overwrite existing points with the same ID.

Batching: OpenAI allows up to 2048 texts per request.
We use batches of 100 to stay well within limits and avoid timeouts.
"""

import uuid
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from config import (
    OPENAI_API_KEY,
    EMBEDDING_MODEL,
    QDRANT_URL,
    QDRANT_HOST,
    QDRANT_PORT,
    QDRANT_API_KEY,
    COLLECTION_NAME,
)

EMBEDDING_DIM = 1536   # text-embedding-3-small output size
BATCH_SIZE = 100


def _get_clients() -> tuple[OpenAI, QdrantClient]:
    openai = OpenAI(api_key=OPENAI_API_KEY)
    if QDRANT_URL:
        qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    else:
        qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY)
    return openai, qdrant


def _ensure_collection(qdrant: QdrantClient) -> None:
    """Create the Qdrant collection if it doesn't exist yet."""
    existing = [c.name for c in qdrant.get_collections().collections]
    if COLLECTION_NAME not in existing:
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
        )
        print(f"[embedder] Created collection '{COLLECTION_NAME}'")
    else:
        print(f"[embedder] Collection '{COLLECTION_NAME}' already exists")


def _embed_batch(openai: OpenAI, texts: list[str]) -> list[list[float]]:
    response = openai.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]


def embed_and_upload(chunks: list[dict]) -> None:
    """
    Embed all chunks and upload to Qdrant.

    Each Qdrant point stores:
      vector  : the embedding
      payload : the chunk text + metadata (used for citation in answers)
    """
    openai, qdrant = _get_clients()
    _ensure_collection(qdrant)

    total = len(chunks)
    uploaded = 0

    for batch_start in range(0, total, BATCH_SIZE):
        batch = chunks[batch_start : batch_start + BATCH_SIZE]
        texts = [c["text"] for c in batch]

        vectors = _embed_batch(openai, texts)

        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "text": chunk["text"],
                    **chunk["metadata"],
                },
            )
            for chunk, vector in zip(batch, vectors)
        ]

        qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
        uploaded += len(batch)
        print(f"[embedder] Uploaded {uploaded}/{total} chunks")

    print(f"[embedder] Done. {total} chunks in Qdrant collection '{COLLECTION_NAME}'")
