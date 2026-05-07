from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_splitter():
    return RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap=50, 
                                           length_function = len, separators = ["\n\n", "\n", ". ", " ", ""] ) 



def chunk_document(doc: dict) -> list[str]:
    splitter = get_splitter()
    all_chunks = []

    for page in doc['pages']:
        chunks = splitter.split_text(page["text"])

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "chunk_id": f"{doc['filename']}_p{page['page']}_c{i}",
                "text": chunk,
                "metadata": {
                "source": doc["filename"],
                "page": page["page"],
                "chunk_index": i,
                "char_count": len(chunk) }
            })

    return all_chunks


def chunk_all_documents(docs : list[dict]) -> list[dict]:
    all_chunks = []
    for doc in docs:
        chunks = chunk_document(doc)
        all_chunks.extend(chunks)
        print(f"  {doc['filename']} → {len(chunks)} chunks")

    return all_chunks

