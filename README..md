# 🕌 Islamic Finance AI Assistant

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/GPT--4o_mini-412991?style=for-the-badge&logo=openai&logoColor=white)
![Qdrant](https://img.shields.io/badge/Qdrant-DC244C?style=for-the-badge&logo=qdrant&logoColor=white)
![AWS](https://img.shields.io/badge/AWS_Free_Tier-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Tavily](https://img.shields.io/badge/Tavily_Search-00A67E?style=for-the-badge&logoColor=white)

**An AI-powered Islamic Finance assistant that answers Shariah-compliant finance questions with verified source citations from the Quran, Hadith, AAOIFI standards, BNM regulations, and trusted scholar opinions.**

[Features](#-features) • [Architecture](#-architecture) • [Tech Stack](#-tech-stack) • [Getting Started](#-getting-started) • [Project Structure](#-project-structure) • [Usage](#-usage)

</div>

---

## 📖 Overview

Islamic Finance AI is a domain-specific question-answering system built on a **hybrid RAG (Retrieval-Augmented Generation)** pipeline. It combines structured document retrieval with live web search to deliver accurate, citation-backed answers strictly within the Islamic finance domain.

The system uses **Flat RAG** for high-volume structured sources like the Quran and Hadith, and **RAPTOR** (Recursive Abstractive Processing for Tree-Organized Retrieval) for hierarchical sources like AAOIFI standards and scholar opinions — matching the indexing strategy to the nature of each source.

---

## ✨ Features

- 📚 **Multi-source Knowledge Base** — Quran, Hadith, AAOIFI standards, BNM regulations, and scholar interpretations
- 🌲 **Hybrid RAG Indexing** — Flat RAG for Quran/Hadith, RAPTOR tree-based indexing for AAOIFI and scholar opinions
- 🔍 **Smart Web Search** — Tavily-powered live search triggered only for scholar opinions and fatwas, restricted to trusted Islamic finance domains
- 📌 **Source Citations** — Every answer includes inline citations (Quran verse, Hadith reference, AAOIFI standard number, or scholar name)
- 🚫 **Domain Guardrails** — Politely declines questions outside Islamic finance
- 🌐 **Web Interface** — Clean Flask-based UI for easy interaction
- ☁️ **Cloud Deployed** — Hosted on AWS Free Tier (EC2 + S3)

---

## 🏗 Architecture

```
User Query
     │
     ▼
┌─────────────────────────────────────────┐
│           Query Classification           │
│  Is this about scholar opinions/fatwas? │
└──────────────┬──────────────────────────┘
               │
       ┌───────┴────────┐
       │                │
      YES               NO
       │                │
       ▼                ▼
 Qdrant +          Qdrant Only
 Tavily Search     (Flat RAG /
 (Trusted          RAPTOR)
  Domains)
       │                │
       └───────┬────────┘
               │
               ▼
     ┌──────────────────┐
     │  Data Augmentation│
     │  + Context Build  │
     └────────┬─────────┘
              │
              ▼
     ┌──────────────────┐
     │  GPT-4o mini LLM  │
     └────────┬─────────┘
              │
              ▼
     Answer with Citations
```

### Indexing Strategy by Source

| Source | Method | Reason |
|--------|---------|--------|
| 📖 Quran | Flat RAG | Large dataset, verse-level retrieval |
| 📜 Hadith | Flat RAG | Similar structure to Quran |
| 🎓 Scholar Opinions | RAPTOR + Tavily | Contextual, argumentative, needs live updates |
| 📋 AAOIFI Standards | RAPTOR | Hierarchical clause structure |
| 🏦 BNM Documents | RAPTOR | Regulatory hierarchical structure |

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|-----------|
| **LLM** | OpenAI GPT-4o mini |
| **Vector Database** | Qdrant |
| **Embeddings** | OpenAI Embeddings |
| **Web Search** | Tavily API (restricted domains) |
| **RAG Framework** | LangChain / LlamaIndex |
| **Tree Indexing** | RAPTOR |
| **Web Framework** | Flask |
| **Deployment** | AWS EC2 Free Tier + S3 |
| **Language** | Python 3.10+ |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- OpenAI API key
- Qdrant instance (local or cloud)
- Tavily API key
- AWS account (for deployment)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/harithamiir/islamicFinance_AI.git
cd islamicFinance_AI
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up environment variables**
```bash
cp .env.example .env
```

Edit `.env` with your keys:
```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
TAVILY_API_KEY=your_tavily_api_key
```

**4. Add your documents**

Place your source documents in the following structure:
```
data/
└── raw/
    ├── quran/        # Quran translations (.txt or .pdf)
    ├── hadith/       # Hadith collections (.txt or .pdf)
    ├── scholar/      # Scholar interpretations (.txt or .pdf)
    ├── aaoifi/       # AAOIFI standards (.txt or .pdf)
    └── bnm/          # BNM regulatory documents (.txt or .pdf)
```

**5. Run ingestion pipeline**
```bash
python -c "from pipeline import ingest; ingest('data/raw')"
```

**6. Start the web app**
```bash
python web_app.py
```

Visit `http://localhost:5000` in your browser.

---

## 📁 Project Structure

```
islamicFinance_AI/
├── src/
│   ├── ingestion/
│   │   ├── loader.py        # Document loading
│   │   ├── chunker.py       # Chunking strategy (Flat + RAPTOR)
│   │   └── embedder.py      # Embedding + Qdrant upload
│   ├── retrieval/
│   │   └── retriever.py     # Qdrant retrieval
│   └── generation/
│       └── generator.py     # GPT-4o mini answer generation
├── templates/               # Flask HTML templates
├── app.py                   # Main app entry point
├── pipeline.py              # Ingestion + Query orchestration
├── web_app.py               # Flask web server
├── config.py                # Configuration settings
├── test_output.py           # Pipeline testing
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
└── .gitignore
```

---

## 💬 Usage

**Example queries the AI can answer:**

- *"Is a conventional mortgage permissible in Islamic finance?"*
- *"What does the Quran say about riba?"*
- *"What is the AAOIFI standard for Murabaha?"*
- *"What is the difference between Musharakah and Mudharabah?"*
- *"What is Bank Negara Malaysia's ruling on Tawarruq?"*
- *"What do scholars say about cryptocurrency in Islamic finance?"*

**The AI will always:**
- Cite its source (Quran verse, Hadith, AAOIFI standard number, scholar name)
- Decline questions outside Islamic finance
- Search trusted scholar websites for fatwa-related queries

---

## 🌐 Trusted Web Search Domains

For scholar opinions and fatwas, web search is restricted to:

- [isra.my](https://isra.my) — International Shariah Research Academy
- [muftitaqiusmani.com](https://muftitaqiusmani.com) — Mufti Taqi Usmani
- [islamqa.info](https://islamqa.info) — IslamQA
- [daralifta.gov.eg](https://daralifta.gov.eg) — Dar al-Ifta Egypt
- [iifa-oic.org](https://iifa-oic.org) — OIC Fiqh Academy

---

## ☁️ Deployment

This project is deployed on **AWS Free Tier**:

- **EC2 t2.micro** — hosts the Flask app and Qdrant
- **S3** — stores source documents

---

## 📊 Evaluation

Pipeline quality is measured using **RAGAS** metrics:

| Metric | Description |
|--------|-------------|
| Faithfulness | Is the answer grounded in retrieved documents? |
| Answer Relevancy | Does the answer address the question? |
| Context Precision | Were the right chunks retrieved? |
| Context Recall | Were all relevant chunks retrieved? |

---

## ⚠️ Disclaimer

This AI assistant is for **educational purposes only**. For official Islamic finance rulings and fatwas, please consult a qualified Shariah scholar.

---

## 👤 Author

**Harith Amir**
- GitHub: [@harithamiir](https://github.com/harithamiir)

---

<div align="center">
Built with ❤️ for the Islamic Finance community
</div>
