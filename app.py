"""
app.py — Command-line interface for the Islamic Finance AI assistant.

Usage:
  python app.py                  # Start interactive chat
  python app.py --ingest         # Load documents from data/raw/ into Qdrant
  python app.py --ingest --dir path/to/docs   # Custom document directory
"""

import argparse
import sys
from pipeline import ingest, ask


WELCOME = """
╔══════════════════════════════════════════════════════╗
║         Islamic Finance AI Assistant                 ║
║  Answers based solely on Quran, Hadith,              ║
║  Scholar interpretations, and AAOIFI standards.      ║
║  Type 'quit' or 'exit' to end the session.           ║
╚══════════════════════════════════════════════════════╝
"""


def run_chat() -> None:
    print(WELCOME)
    while True:
        try:
            question = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break

        if not question:
            continue

        if question.lower() in {"quit", "exit"}:
            print("Goodbye.")
            break

        print("\nAssistant: ", end="", flush=True)
        answer = ask(question)
        print(answer)
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Islamic Finance AI Assistant")
    parser.add_argument(
        "--ingest",
        action="store_true",
        help="Ingest documents from the data directory into Qdrant",
    )
    parser.add_argument(
        "--dir",
        default="data/raw",
        help="Document directory to ingest (default: data/raw)",
    )
    args = parser.parse_args()

    if args.ingest:
        ingest(data_dir=args.dir)
        print("Documents ingested. Run 'python app.py' to start chatting.")
        sys.exit(0)

    run_chat()


if __name__ == "__main__":
    main()
