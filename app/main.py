from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

from rag_chain import create_rag_chain, preprocess_query
from sql_agent import create_sql_agent

FINAL_PROMPT = PromptTemplate.from_template("""
You are a synthesis agent.

Given a user question and the outputs from a SQL agent and a RAG agent, produce the best final answer.
- Prefer factual results from SQL output when relevant.
- Use RAG output for definitions or explanations.
- If there is a conflict, mention it briefly and choose the most reliable source.

Question:
{question}

SQL output:
{sql_output}

RAG output:
{rag_output}

Final answer:
""")


def _extract_agent_text(result) -> str:
    if isinstance(result, str):
        return result
    if isinstance(result, dict):
        if "output" in result:
            return str(result["output"])
        if "messages" in result and result["messages"]:
            last_message = result["messages"][-1]
            if hasattr(last_message, "content"):
                return str(last_message.content)
            if isinstance(last_message, dict) and "content" in last_message:
                return str(last_message["content"])
        if "content" in result:
            return str(result["content"])
    return str(result)


def _run_sql_agent(question: str) -> str:
    agent = create_sql_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    return _extract_agent_text(result)


def _run_rag_chain(question: str) -> str:
    chain = create_rag_chain()
    return chain.invoke(preprocess_query(question))


def answer_question(question: str) -> str:
    # llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0) 
    parallel = RunnableParallel(
        question=RunnablePassthrough(),
        sql_output=RunnableLambda(_run_sql_agent),
        rag_output=RunnableLambda(_run_rag_chain),
    )
    final_chain = parallel | FINAL_PROMPT | llm | StrOutputParser()
    return final_chain.invoke(question)


if __name__ == "__main__":
    question = "who is the coach of Leviatán?"
    print(answer_question(question))