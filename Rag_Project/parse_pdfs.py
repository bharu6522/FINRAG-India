import os 
import PyPDF2 
import re 
# from langchain_community.document_loaders import PyPDFLoader

from dotenv import load_dotenv 

load_dotenv()

pdf_dir = "D:\Gitlab_repos\personal\LangChain\Rag_Project\PDFs"

def parse_pdf(filepath: str ) -> dict:
    text_pages = []
    with open(filepath, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        num_pages = len(reader.pages)
        print(f"  [{os.path.basename(filepath)}] → {num_pages} pages")

        for page_num, page in enumerate(reader.pages):
            raw_text = page.extract_text()
            if raw_text:
                text_pages.append({
                    "page" : page_num + 1, 
                    "text" : raw_text
                })

        
    return {
        "filename": os.path.basename(filepath),
        "filepath": filepath,
        "total_pages": num_pages,
        "pages": text_pages
    }

def parse_all_pdfs(pdf_dir: str) -> list[dict] : 
    all_docs = []
    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
    print(f"Found {len(pdf_files)} PDFs to parse...\n")

    for pdf in pdf_files:
        filepath = os.path.join(pdf_dir,pdf)
        doc = parse_pdf(filepath)
        all_docs.append(doc)


    return all_docs


if __name__ == "__main__":
    docs = parse_all_pdfs(pdf_dir)
    print(f"\n✅ Parsed {len(docs)} documents successfully.")

