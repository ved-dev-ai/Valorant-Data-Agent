# rag/retriever.py

import os

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

CHROMA_PATH = "./app/rag/index/chroma"
HF_CACHE_DIR = "./app/cache/huggingface"


def get_retriever():

    os.makedirs(HF_CACHE_DIR, exist_ok=True)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        cache_folder=HF_CACHE_DIR
    )

    vectordb = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )

    # retriever = vectordb.as_retriever(
    #     search_type="similarity",
    #     search_kwargs={"k": 4}
    # )
    
    retriever = vectordb.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 4, "fetch_k": 20}
    )

    return retriever
