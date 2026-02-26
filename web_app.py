"""
web_app.py — Flask web interface for the Islamic Finance AI assistant.

Run:
    python web_app.py

Then open: http://localhost:5000
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, render_template, request, jsonify
from pipeline import ask

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()
    question = (data or {}).get("question", "").strip()

    if not question:
        return jsonify({"answer": "Please enter a question."}), 400

    try:
        answer = ask(question)
        return jsonify({"answer": answer})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"answer": f"Server error: {e}"}), 500


if __name__ == "__main__":
    print("Starting Islamic Finance AI at http://localhost:5000")
    app.run(debug=False, port=5000)
