"""Measure retrieval quality on a list of known questions.

hit@k = share of questions where the correct source file AND an expected keyword
appear among the top-k retrieved chunks. Edit eval_questions.json to match YOUR
documents, then report the number you actually get.
"""
import json
import sys

from rag import RagPipeline


def main(folder="sample_docs", qfile="eval_questions.json", k=3):
    rag = RagPipeline()
    n_chunks = rag.index_folder(folder)
    questions = json.load(open(qfile))
    hits = 0
    for item in questions:
        results = rag.retrieve(item["q"], k)
        ok = any(
            c.source == item["source"] and all(kw in c.text.lower() for kw in item["keywords"])
            for c, _ in results
        )
        hits += ok
        print(("PASS " if ok else "FAIL ") + item["q"])
    print(f"\nChunks indexed: {n_chunks}")
    print(f"hit@{k}: {hits}/{len(questions)} = {100 * hits / len(questions):.0f}%")


if __name__ == "__main__":
    main(*sys.argv[1:2]) if len(sys.argv) > 1 else main()
