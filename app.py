"""Web app: upload PDFs, ask questions, see answers with sources.  Run: python app.py"""
import os
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename

from rag import RagPipeline
from rag import llm

BASE = Path(__file__).parent
UPLOADS = BASE / "uploads"
SAMPLES = BASE / "sample_docs"
UPLOADS.mkdir(exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024  # 25 MB per request
rag = RagPipeline()


def reindex():
    pdfs = sorted(UPLOADS.glob("*.pdf")) or sorted(SAMPLES.glob("*.pdf"))
    n = rag.index_files(pdfs)
    return [p.name for p in pdfs], n


@app.get("/")
def home():
    files, n = reindex() if rag.retriever is None else (sorted({c.source for c in rag.chunks}), len(rag.chunks))
    return render_template("index.html", files=files, n_chunks=n, llm_on=llm.llm_available())


@app.post("/upload")
def upload():
    saved = []
    for f in request.files.getlist("files"):
        name = secure_filename(f.filename or "")
        if not name.lower().endswith(".pdf"):
            continue
        f.save(UPLOADS / name)
        saved.append(name)
    if not saved:
        return jsonify(error="Please upload at least one .pdf file."), 400
    files, n = reindex()
    return jsonify(files=files, chunks=n)


@app.post("/ask")
def ask():
    question = (request.get_json(silent=True) or {}).get("question", "").strip()
    if not question:
        return jsonify(error="Please type a question."), 400
    if rag.retriever is None:
        reindex()
    return jsonify(rag.ask(question))


@app.post("/reset")
def reset():
    for p in UPLOADS.glob("*.pdf"):
        p.unlink()
    files, n = reindex()
    return jsonify(files=files, chunks=n)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 5000)), debug=False)
