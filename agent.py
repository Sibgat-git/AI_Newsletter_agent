from dotenv import load_dotenv
from langchain_perplexity import ChatPerplexity
from langchain_community.document_loaders import  TextLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import Tool
from langchain.agents import(
    AgentExecutor,
    create_react_agent
)



load_dotenv()

llm = ChatPerplexity(
    model="llama-3.1-sonar-small-128k-online"
    temperature= 0.7,
    api_key="PERPLEXITY_API_KEY"
)


def webscrape_to_text(*arg, **kwargs):
    """returns the information on any querry."""

    query= input("What do you wanna know?")



Agent= create_react_agent(
    llm=llm,

)


the_retriever



