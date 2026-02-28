# Islamic Finance AI — Project Memory

## Stack
- Python, Flask, OpenAI (GPT-4o mini + text-embedding-3-small), Qdrant Cloud, Tavily
- All keys in `.env` (never `.env.example`)

## Key files
- `pipeline.py` — orchestrator, two functions: `ingest()` and `ask()`
- `config.py` — all constants (API keys, chunk size, Qdrant settings, Tavily domains)
- `src/ingestion/` — loader, chunker, embedder
- `src/retrieval/retriever.py` — Qdrant search using `query_points()` (not `.search()` — removed in qdrant-client 1.9+)
- `src/retrieval/web_search.py` — Tavily search, only triggered for scholar/fatwa questions
- `src/generation/generator.py` — prompt builder + GPT-4o mini call
- `web_app.py` — Flask UI on port 5000
- `templates/index.html` — chat UI

## Known issues fixed
- qdrant-client 1.9+ removed `.search()` — use `.query_points()`, results in `.points`
- QDRANT_URL must be set in `.env` (not commented out) for Qdrant Cloud to work
- Topic guard keywords in `generator.py` must include common question words (ruling, scholar, crypto, etc.) or questions get declined before reaching the LLM

## Citation formats
- Quran: `[Source: Quran — Surah X, Ayah Y]`
- AAOIFI/Hadith/Scholar: `[Source: TYPE — filename]`
- Web (Tavily): `[Source: SCHOLAR_WEB — https://...]`

## Quran data format
Pipe-separated `.txt` in `data/raw/quran/`: `surah|ayah|text` (one ayah per line)
Loader auto-detects this format and stores surah/ayah as metadata.

## User preferences
- Explain before executing
- Keep code clean and simple
- Don't execute unless asked
