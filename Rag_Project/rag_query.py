import os 
import json 
import numpy as np
import faiss 
from openai import OpenAI
from embed_store import load_store, embed_model
from dotenv import load_dotenv

load_dotenv()

client = OpenAI() # api_key= os.environ["OPEN_API_KEY"]

TOP_K = 5 # number of chunks need to retrieve 
gpt_model = "gpt-4o-mini"
max_tokens = 800 

SYSTEM_PROMPT = """You are a financial analyst assistant specializing in Indian \
regulatory documents (RBI, SEBI) and corporate annual reports.

Answer questions ONLY using the provided context chunks.
- Be precise and cite the source document and page for each claim.
- If the context doesn't contain enough information, say so clearly.
- Format numbers and financial data clearly (use ₹ symbol for INR).
- Keep answers concise but complete."""


def embed_query(query: str) -> np.ndarray:
    response = client.embeddings.create(model= embed_model, input= [query] )
    vec = np.array(response.data[0].embedding, dtype= "float32").reshape(1,-1)
    faiss.normalize_L2(vec)

    return vec 


def retrieve_chunks(query: str, index, metadata: list[dict], top_k: int = TOP_K) -> list[dict] :
    query_vec= embed_query(query)
    scores, indices = index.search(query_vec, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        chunk = metadata[idx].copy()
        chunk["similarity_score"] = round(float(score),4)

        results.append(chunk)

    return results


def build_context(chunks: list[dict]) -> str:

    parts = []
    for i, c in enumerate(chunks,1):
        parts.append(f"[{i}] Source: {c['source']} | Page: {c['page']} "
            f"| Score: {c['similarity_score']}\n{c['text']}")

    return "\n\n---\n\n".join(parts)


def ask(query: str, index, metadata: list[dict], verbose: bool = True) -> str:

    chunks = retrieve_chunks(query, index, metadata)

    if verbose:
        print(f"\n Retrieved {len(chunks)} chunks:")

        for c in chunks:
            print(f"   [{c['similarity_score']:.3f}] "
                  f"{c['source']} p.{c['page']}")

    context = build_context(chunks)
    user_message = f"""Context from financial documents:

{context}

---

Question: {query}

Answer based only on the context above. Cite sources."""
    
    response = client.chat.completions.create(model= gpt_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_message}
        ],
        max_tokens= max_tokens,
        temperature=0.2)
    
    answer = response.choices[0].message.content

    return answer 


def interactive_chat():
    print("Loading Vector Store")
    index, metadata = load_store()

    print(f"  {index.ntotal} vectors ready.\n")
    print(" Financial RAG Assistant (type 'quit' to exit)\n")
    print("=" * 60)

    while True:
        query = input("\n❓ Your question: ").strip()
        if query.lower() in ("quit", "exit", "q"):
            break
        if not query:
            continue

        answer = ask(query, index, metadata)
        print(f"\n🤖 Answer:\n{answer}")
        print("\n" + "=" * 60)


if __name__ == "__main__":
    interactive_chat()
