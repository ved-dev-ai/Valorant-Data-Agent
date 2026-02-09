from rag_chain import create_rag_chain
from rag_chain import preprocess_query

rag_chain = create_rag_chain()

while(True):
    question = input("Enter your question: ")
    print(
        rag_chain.invoke(
            preprocess_query(question)
        )
    )