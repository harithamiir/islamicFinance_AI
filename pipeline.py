"""
pipeline.py — Orchestrates ingestion and query answering.

Two public functions:
  ingest(data_dir)  : run once to load, chunk, embed, and store documents
  ask(question)     : run on every user question to retrieve and generate an answer
"""

import sys
import os

# Allow imports from the project root
sys.path.insert(0, os.path.dirname(__file__))

from src.ingestion.loader import load_documents
from src.ingestion.chunker import chunk_documents
from src.ingestion.embedder import embed_and_upload
from src.retrieval.retriever import retrieve
from src.retrieval.web_search import search_scholar_web
from src.generation.generator import generate_answer

_SCHOLAR_FATWA_KEYWORDS = [
    "fatwa", "fatwas", "scholar", "scholars", "opinion", "ruling", "rulings",
    "mufti", "sheikh", "shaykh", "contemporary", "modern ruling", "sharia board",
    "fiqh council", "what do scholars", "what does islam say", "is it permissible",
    "is it allowed", "can a muslim", "hukm", "permissible", "prohibited",
]


def _is_scholar_fatwa_question(question: str) -> bool:
    """Return True if the question is asking for scholar opinions or fatwas."""
    q_lower = question.lower()
    return any(kw in q_lower for kw in _SCHOLAR_FATWA_KEYWORDS)


def ingest(data_dir: str = "data/raw") -> None:
    """
    Full ingestion pipeline: load → chunk → embed → upload to Qdrant.

    Run this once after adding or updating documents.

    Args:
        data_dir : path to the folder containing source documents.
                   Sub-folders should be named: quran, hadith, scholar, aaoifi
    """
    print("\n=== INGESTION PIPELINE ===")
    documents = load_documents(data_dir)

    if not documents:
        print(f"No documents found in '{data_dir}'. "
              "Add .txt or .pdf files to subfolders: quran/, hadith/, scholar/, aaoifi/")
        return

    chunks = chunk_documents(documents)
    embed_and_upload(chunks)
    print("=== INGESTION COMPLETE ===\n")


def ask(question: str) -> str:
    """
    Query pipeline: retrieve relevant chunks → generate answer with citations.

    If the question is about scholar opinions or fatwas, also searches Tavily
    across trusted Islamic scholar domains and combines results with Qdrant.

    Args:
        question : the user's question

    Returns:
        Answer string with inline citations.
    """
    chunks = retrieve(question)

    if _is_scholar_fatwa_question(question):
        print("[pipeline] Scholar/fatwa question detected — adding web search")
        web_chunks = search_scholar_web(question)
        chunks = chunks + web_chunks

    answer = generate_answer(question, chunks)
    return answer
