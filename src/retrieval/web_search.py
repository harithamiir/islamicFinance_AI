"""
web_search.py — Tavily web search restricted to trusted Islamic scholar domains.

Only called when the question is detected as being about scholar opinions or fatwas.
Returns results in the same chunk dict format as retriever.py so the generator
receives a single uniform list regardless of source.

Citation format for web results:
  [Source: SCHOLAR_WEB — https://islamqa.info/en/...]
"""

from tavily import TavilyClient
from config import TAVILY_API_KEY, TAVILY_DOMAINS


def search_scholar_web(query: str, max_results: int = 3) -> list[dict]:
    """
    Search trusted Islamic scholar domains via Tavily.

    Args:
        query       : the user's question
        max_results : number of web results to return (kept low to avoid
                      overwhelming the Qdrant results)

    Returns:
        List of chunk dicts matching the same structure as retriever.retrieve().
        Returns empty list if TAVILY_API_KEY is not set or search fails.
    """
    if not TAVILY_API_KEY:
        print("[web_search] TAVILY_API_KEY not set — skipping web search")
        return []

    try:
        client = TavilyClient(api_key=TAVILY_API_KEY)
        response = client.search(
            query=query,
            include_domains=TAVILY_DOMAINS,
            max_results=max_results,
            search_depth="advanced",
            include_answer=True,   # Tavily synthesises a clean answer from results
        )

        results = []

        # Add Tavily's synthesised answer as the first chunk if available
        tavily_answer = (response.get("answer") or "").strip()
        if tavily_answer:
            results.append({
                "text": tavily_answer,
                "score": 1.0,
                "source_type": "scholar_web",
                "filename": "Tavily synthesis from scholar domains",
                "chunk_index": 0,
                "surah": None,
                "ayah": None,
            })

        for item in response.get("results", []):
            content = item.get("content", "").strip()
            url = item.get("url", "")
            score = round(item.get("score", 0.0), 4)

            if not content:
                continue

            results.append({
                "text": content,
                "score": score,
                "source_type": "scholar_web",
                "filename": url,
                "chunk_index": 0,
                "surah": None,
                "ayah": None,
            })

        print(f"[web_search] Retrieved {len(results)} results from scholar domains")
        for i, r in enumerate(results):
            print(f"[web_search] Result {i+1}: {r['filename']}")
            print(f"[web_search] Content preview: {r['text'][:300]}\n")
        return results

    except Exception as e:
        print(f"[web_search] Search failed: {e}")
        return []
