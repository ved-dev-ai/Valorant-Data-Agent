import os
from langchain.agents import create_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from sqlalchemy import create_engine

from dotenv import load_dotenv
load_dotenv()

def create_sql_agent(llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)):
    
    db_url = "sqlite:///warehouse/vct.sqlite"
    engine = create_engine(db_url)
    db = SQLDatabase(engine)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    tools = toolkit.get_tools()

    system_prompt = """
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run,
then look at the results of the query and return the answer. Unless the user
specifies a specific number of examples they wish to obtain, always limit your
query to at most {top_k} results.

You can order the results by a relevant column to return the most interesting
examples in the database. Never query for all the columns from a specific table,
only ask for the relevant columns given the question.

You MUST double check your query before executing it. If you get an error while
executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
database.

To start you should ALWAYS look at the tables in the database to see what you
can query. Do NOT skip this step.

Then you should query the schema of the most relevant tables.
""".format(
        dialect=db.dialect,
        top_k=5,
    )

    return create_agent(
        llm,
        tools,
        system_prompt=system_prompt,
    )
