# rag/rag_chain.py

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from rag.retriever import get_retriever

import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq( model="openai/gpt-oss-20b", temperature=0 )

PROMPT = PromptTemplate.from_template("""
You are a helpful esports analyst.

Use the context below to answer the question.
If the answer is not in the context, say "I don't have enough information."

Context:
{context}

Question:
{question}
""")

nltk.download('stopwords')
nltk.download('punkt')

def preprocess_query(query):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(query.lower())
    keywords = [w for w in tokens if w.isalnum() and w not in stop_words]
    return ' '.join(keywords)

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)


def create_rag_chain(llm=llm):

    retriever = get_retriever()

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | PROMPT
        | llm
        | StrOutputParser()
    )

    return chain
