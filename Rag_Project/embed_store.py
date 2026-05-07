import os 
import json 
import time 
import numpy as np
import faiss 
from openai import OpenAI

client = OpenAI(api_key= os.environ["OPENAI_API_KEY"])

embed_model = "text-embedding-3-small"
chunks_file = "chunks.json"
store_dir = "vector_store"
batch_size = 50 

def embed_texts(texts: list[str]) -> list[list[float]] :
    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i: i+batch_size]
        print(f"  Embedding batch {i // batch_size + 1} "
              f"({len(batch)} chunks)...")
        
        response = client.embeddings.create(model= embed_model, input= batch)
        batch_embeddings = [item.embedding for item in response.data]
        all_embeddings.extend(batch_embeddings)
        time.sleep(0.3)

        return all_embeddings
    


def build_faiss_index(embeddings: list[list[float]]) -> faiss.Index:
    dim = len(embeddings[0])
    matrix = np.array(embeddings, dtype= 'float32')

    faiss.normalize_L2(matrix) # normalizing cosine similarity 
    index = faiss.IndexFlatIP(dim)
    index.add(matrix)
    print(f"  FAISS index built: {index.ntotal} vectors, dim={dim}")
    return index

def save_store(index, chunks: list[dict]):
    os.makedirs(store_dir, exist_ok= True)
    faiss.write_index(index, f"{store_dir}/index.faiss")

    metadata = [c["metadata"] | {"text": c["text"]} for c in chunks]
    with open(f"{store_dir}/metadata.json","w") as f:
        json.dump(metadata, f, indent=2)

    print(f"  Saved index + metadata to '{store_dir}/'")



def load_store():

    index = faiss.read_index(f"{store_dir}/index.faiss")
    with open(f"{store_dir}/metadata.json") as f:
        metadata = json.load(f)

    return index, metadata


def run_embedding_pipeline():
    print("Loading Chunks.......")
    with open(chunks_file) as f:
        chunks = json.load(f)

    print(f"    {len(chunks)} chunks loaded\n")

    print(f"Embedding chunks with OpenAI\n")
    texts = [c["text"] for c in chunks]
    embeddings = embed_texts(texts)

    print("\n Building Faiss Vector Store")
    index= build_faiss_index(embeddings)
    save_store(index, chunks) 

    print(f"\n✅ Embedding complete! {len(chunks)} vectors stored.")
    return index, chunks


if __name__ == '__main__':
    run_embedding_pipeline()
