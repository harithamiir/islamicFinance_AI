"""
generator.py — Build the prompt and call GPT-4o mini.

Flow:
  1. Topic guard: reject questions unrelated to Islamic finance.
  2. Build a context block from retrieved chunks, each labelled with its source.
  3. Send system prompt + context + user question to GPT-4o mini.
  4. Return the answer text.

The model is instructed to:
  - Answer ONLY from the provided context (no external knowledge).
  - Cite every claim with its source type and filename.
  - Politely decline if the question is not about Islamic finance.
"""

from openai import OpenAI
from config import OPENAI_API_KEY, CHAT_MODEL

_client = OpenAI(api_key=OPENAI_API_KEY)

_SYSTEM_PROMPT = """You are an Islamic Finance AI assistant.

Your sole purpose is to answer questions about Islamic finance, including:
- Quranic verses related to finance and trade
- Hadiths related to financial conduct
- Rulings from Islamic scholars on financial matters
- AAOIFI (Accounting and Auditing Organization for Islamic Financial Institutions) standards

STRICT RULES you must follow:
1. Answer ONLY using the context passages provided below. Do not use any outside knowledge.
2. Every factual claim in your answer MUST be followed by a citation in one of these formats:
   - Quran:   [Source: Quran — Surah X, Ayah Y]
   - Hadith:  [Source: HADITH — filename]
   - Scholar: [Source: SCHOLAR — filename]
   - AAOIFI:  [Source: AAOIFI — filename]
3. If the provided context does not contain enough information to answer the question,
   say: "I could not find sufficient information in my sources to answer this question."
4. If the question is NOT about Islamic finance, respond with:
   "I can only assist with Islamic finance topics. Please ask a question related to
    Islamic finance, banking, transactions, or related Sharia rulings."
5. Do not speculate, infer, or add information beyond what the context states.
6. Write in clear, professional English.
"""


def _is_islamic_finance_topic(question: str) -> bool:
    """
    Lightweight keyword guard before sending to the LLM.
    This avoids wasting API calls on clearly off-topic questions.
    The LLM prompt also handles this as a second layer.
    """
    keywords = [
        "riba", "interest", "zakat", "sukuk", "murabaha", "ijara", "musharaka",
        "mudaraba", "halal", "haram", "sharia", "shariah", "islamic finance",
        "islamic banking", "profit", "loss", "trade", "contract", "loan",
        "mortgage", "investment", "takaful", "insurance", "quran", "hadith",
        "aaoifi", "fiqh", "fatwa", "finance", "bank", "money", "debt",
        "transaction", "sale", "purchase", "exchange", "commodity",
    ]
    q_lower = question.lower()
    return any(kw in q_lower for kw in keywords)


def _build_context_block(retrieved_chunks: list[dict]) -> str:
    """Format retrieved chunks into a numbered context block for the prompt."""
    lines = []
    for i, chunk in enumerate(retrieved_chunks, start=1):
        if chunk["source_type"] == "quran" and chunk.get("surah") and chunk.get("ayah"):
            source_label = f"Quran — Surah {chunk['surah']}, Ayah {chunk['ayah']}"
        else:
            source_label = f"{chunk['source_type'].upper()} — {chunk['filename']}"
        lines.append(f"[{i}] {source_label}\n{chunk['text']}\n")
    return "\n".join(lines)


def generate_answer(question: str, retrieved_chunks: list[dict]) -> str:
    """
    Generate an answer for the given question using retrieved context.

    Args:
        question         : the user's question
        retrieved_chunks : list of chunk dicts from the retriever

    Returns:
        Answer string (may include a polite decline if off-topic).
    """
    # First layer: fast keyword check
    if not _is_islamic_finance_topic(question):
        return (
            "I can only assist with Islamic finance topics. "
            "Please ask a question related to Islamic finance, banking, "
            "transactions, or related Sharia rulings."
        )

    if not retrieved_chunks:
        return (
            "I could not find relevant information in my sources to answer this question."
        )

    context_block = _build_context_block(retrieved_chunks)

    user_message = f"""CONTEXT PASSAGES:
{context_block}

QUESTION: {question}

Answer the question using only the context passages above. Cite every claim."""

    response = _client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.0,   # Deterministic — no creative hallucination
        max_tokens=1024,
    )

    return response.choices[0].message.content.strip()
