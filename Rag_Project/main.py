import os
from parse_pdfs  import parse_all_pdfs
from clean_text  import clean_document
from chunk_text  import chunk_all_documents
from embed_store import run_embedding_pipeline
from rag_query   import interactive_chat
import json

PDF_DIR     = r"D:\\Gitlab_repos\\personal\\LangChain\\Rag_Project\\PDFs"
CHUNKS_FILE = "chunks.json"
STORE_DIR   = "vector_store"

def run_full_pipeline():
    # ── Stage 1: Parse ──────────────────────────────────────
    print("=" * 60)
    print("STAGE 1: Parsing PDFs")
    print("=" * 60)
    raw_docs = parse_all_pdfs(PDF_DIR)

    # ── Stage 2: Clean ──────────────────────────────────────
    print("\n" + "=" * 60)
    print("STAGE 2: Cleaning Text")
    print("=" * 60)
    cleaned_docs = [clean_document(doc) for doc in raw_docs]

    # ── Stage 3: Chunk ──────────────────────────────────────
    print("\n" + "=" * 60)
    print("STAGE 3: Chunking (size=500, overlap=50)")
    print("=" * 60)
    chunks = chunk_all_documents(cleaned_docs)
    with open(CHUNKS_FILE, "w") as f:
        json.dump(chunks, f, indent=2)
    print(f"\n  Saved {len(chunks)} chunks → {CHUNKS_FILE}")

    # ── Stage 4: Embed + Store ──────────────────────────────
    print("\n" + "=" * 60)
    print("STAGE 4: Embedding + FAISS Vector Store")
    print("=" * 60)
    run_embedding_pipeline()

    # ── Stage 5: Query ──────────────────────────────────────
    print("\n" + "=" * 60)
    print("STAGE 5: RAG Query Interface")
    print("=" * 60)
    interactive_chat()


if __name__ == "__main__":
    # Set your key: export OPENAI_API_KEY="sk-..."
    run_full_pipeline()