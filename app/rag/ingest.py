# rag/ingest.py

import json
from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters  import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os

DATA_PATH = Path("./app/rag/data/articles.json")

CHROMA_PATH = "./app/rag/index/chroma"
HF_CACHE_DIR = "./app/cache/huggingface"

def chunk_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=500
    )

    return splitter.split_documents(documents)

def load_articles():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = []

    for item in data:
        doc = Document(
            page_content=item["cleaned_content"],
            metadata={
                "title": item["title"],
                "date": item["date"],
                "url": item["url"]
            }
        )
        documents.append(doc)

    return documents

def build_vector_store(chunks):

    os.makedirs(HF_CACHE_DIR, exist_ok=True)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        cache_folder=HF_CACHE_DIR
    )

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )

    print("ChromaDB index built")

def main():
    docs = load_articles()
    chunks = chunk_documents(docs)
    build_vector_store(chunks)


if __name__ == "__main__":
    main()
