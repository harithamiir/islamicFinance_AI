import os
from dotenv import load_dotenv

load_dotenv()

# --- OpenAI ---
OPENAI_API_KEY: str = os.environ["OPENAI_API_KEY"]
EMBEDDING_MODEL: str = "text-embedding-3-small"   # 1536 dimensions, cheap
CHAT_MODEL: str = "gpt-4o-mini"

# --- Qdrant ---
# QDRANT_URL takes priority (Qdrant Cloud). Falls back to host+port for local.
QDRANT_URL: str | None = os.getenv("QDRANT_URL") or None
QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_API_KEY: str | None = os.getenv("QDRANT_API_KEY") or None
COLLECTION_NAME: str = "islamic_finance"

# --- Chunking ---
# 800 tokens ~ 600 words — fits one fatwa or one AAOIFI clause comfortably
CHUNK_SIZE: int = 800
# Overlap keeps context from being cut off at chunk boundaries
CHUNK_OVERLAP: int = 100

# --- Retrieval ---
# How many chunks to pull from Qdrant per question
TOP_K: int = 5

# --- Tavily web search (used for scholar/fatwa questions only) ---
TAVILY_API_KEY: str | None = os.getenv("TAVILY_API_KEY") or None

# Domains restricted for Tavily search
TAVILY_DOMAINS = [
    "isra.my",
    "muftitaqiusmani.com",
    "islamqa.info",
    "daralifta.gov.eg",
    "iifa-oic.org",
]

# --- Source types (used as metadata tags on every chunk) ---
SOURCE_TYPES = ["quran", "hadith", "scholar", "aaoifi", "scholar_web"]
