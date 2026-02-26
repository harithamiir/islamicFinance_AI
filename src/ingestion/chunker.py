"""
chunker.py — Split document text into overlapping token-sized chunks.

Why overlap? If a relevant sentence falls at the end of chunk N,
overlap ensures it also appears at the start of chunk N+1 so it
won't be missed during retrieval.

Each output chunk keeps the parent document's metadata plus a
chunk_index so you can reconstruct ordering if needed.
"""

import tiktoken
from config import CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL

# Use the same tokenizer as the embedding model
_enc = tiktoken.encoding_for_model(EMBEDDING_MODEL)


def _tokenize(text: str) -> list[int]:
    return _enc.encode(text)


def _detokenize(tokens: list[int]) -> str:
    return _enc.decode(tokens)


def chunk_document(doc: dict) -> list[dict]:
    """
    Split a single document dict into chunk dicts.

    Returns a list of chunk dicts, each with:
      text     : the chunk text
      metadata : parent metadata + chunk_index
    """
    tokens = _tokenize(doc["text"])
    chunks = []
    start = 0

    while start < len(tokens):
        end = start + CHUNK_SIZE
        chunk_tokens = tokens[start:end]
        chunk_text = _detokenize(chunk_tokens)

        chunks.append({
            "text": chunk_text,
            "metadata": {
                **doc["metadata"],
                "chunk_index": len(chunks),
            }
        })

        # Move forward by (CHUNK_SIZE - CHUNK_OVERLAP) to create overlap
        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def chunk_documents(documents: list[dict]) -> list[dict]:
    """Chunk all documents and return a flat list of chunk dicts."""
    all_chunks = []
    for doc in documents:
        chunks = chunk_document(doc)
        all_chunks.extend(chunks)
        print(f"[chunker] {doc['metadata']['filename']} → {len(chunks)} chunks")

    print(f"[chunker] Total chunks: {len(all_chunks)}")
    return all_chunks
