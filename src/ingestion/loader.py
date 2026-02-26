"""
loader.py — Read source documents from disk into plain text dicts.

Each document dict has:
  text     : the raw text content
  metadata : citation info that will appear in answers
              source_type : one of quran | hadith | scholar | aaoifi
              filename    : original file name
              surah       : (Quran only) surah number as string
              ayah        : (Quran only) ayah number as string

Supported formats:
  .txt  — plain text, or pipe-separated Quran format (surah|ayah|text)
  .pdf  — text-based PDFs only (not scanned)

Quran pipe format (one ayah per line):
  78|12|We raised over you several secure skies
"""

from pathlib import Path
from pypdf import PdfReader


def _load_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages)


def _is_quran_pipe_format(path: Path) -> bool:
    """Check the first non-empty line to detect surah|ayah|text format."""
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            return len(parts) >= 3 and parts[0].isdigit() and parts[1].isdigit()
    return False


def _load_quran_pipe_txt(path: Path) -> list[dict]:
    """
    Parse a pipe-separated Quran file into one document per ayah.
    Each line: surah_number|ayah_number|ayah_text
    """
    documents = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|", 2)
            if len(parts) < 3:
                continue
            surah, ayah, text = parts[0].strip(), parts[1].strip(), parts[2].strip()
            if not text:
                continue
            documents.append({
                "text": text,
                "metadata": {
                    "source_type": "quran",
                    "filename": path.name,
                    "surah": surah,
                    "ayah": ayah,
                }
            })
    return documents


def load_documents(data_dir: str) -> list[dict]:
    """
    Walk data_dir and load every .txt and .pdf file.

    Folder structure determines source_type:
        data/raw/quran/      → source_type = "quran"
        data/raw/hadith/     → source_type = "hadith"
        data/raw/scholar/    → source_type = "scholar"
        data/raw/aaoifi/     → source_type = "aaoifi"

    Quran .txt files in pipe format are parsed into one document per ayah.

    Returns a list of document dicts.
    """
    documents = []
    root = Path(data_dir)

    for file_path in root.rglob("*"):
        if file_path.suffix not in {".txt", ".pdf"}:
            continue

        source_type = file_path.parent.name.lower()

        # Quran pipe format: parse each ayah as its own document
        if source_type == "quran" and file_path.suffix == ".txt" and _is_quran_pipe_format(file_path):
            ayah_docs = _load_quran_pipe_txt(file_path)
            documents.extend(ayah_docs)
            print(f"[loader] Loaded {file_path.name} → {len(ayah_docs)} ayahs (quran pipe format)")
            continue

        # Standard load for all other files
        if file_path.suffix == ".pdf":
            text = _load_pdf(file_path)
        else:
            text = file_path.read_text(encoding="utf-8")

        if not text.strip():
            print(f"[loader] Skipping empty file: {file_path.name}")
            continue

        documents.append({
            "text": text,
            "metadata": {
                "source_type": source_type,
                "filename": file_path.name,
            }
        })
        print(f"[loader] Loaded {file_path.name} ({source_type})")

    print(f"[loader] Total documents loaded: {len(documents)}")
    return documents
