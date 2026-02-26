"""
test_output.py — Preview what answers look like without running the full pipeline.

Mocks a few retrieved chunks so you can test the generator directly.
Requirements: .env file with OPENAI_API_KEY set.

Run:
    python test_output.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.generation.generator import generate_answer

# --- Mock chunks (simulating what Qdrant would return) ---

MOCK_CHUNKS = [
    {
        "text": "Those who devour usury will not stand except as stands one whom the Evil One by his touch hath driven to madness. That is because they say: Trade is like usury, but Allah hath permitted trade and forbidden usury.",
        "score": 0.91,
        "source_type": "quran",
        "filename": "quran_sahih_international.txt",
        "chunk_index": 0,
        "surah": "2",
        "ayah": "275",
    },
    {
        "text": "O you who have believed, fear Allah and give up what remains of interest, if you should be believers.",
        "score": 0.87,
        "source_type": "quran",
        "filename": "quran_sahih_international.txt",
        "chunk_index": 0,
        "surah": "2",
        "ayah": "278",
    },
    {
        "text": "Murabaha is a sale contract whereby the Islamic bank purchases goods and resells them to the client at cost plus an agreed profit margin. The profit margin must be disclosed to the buyer.",
        "score": 0.83,
        "source_type": "aaoifi",
        "filename": "aaoifi_standard_08_murabaha.pdf",
        "chunk_index": 2,
        "surah": None,
        "ayah": None,
    },
]

# --- Test questions ---

questions = [
    "Is interest (riba) allowed in Islam?",
    "What is Murabaha and how does it work?",
    "What is the capital of France?",
]

print("=" * 60)
for question in questions:
    print(f"\nQ: {question}")
    print("-" * 60)
    answer = generate_answer(question, MOCK_CHUNKS)
    print(f"A: {answer}")
    print("=" * 60)
