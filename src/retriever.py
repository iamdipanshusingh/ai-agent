from langchain.agents import create_agent
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src import model
from src.embeddings import vector_store
from src.loaders import web_loader
from src.tools import retrieve_context


class Agent:
    """Creates an agent with a prompt, to answer queries"""
    def __init__(self):
        # Load and chunk contents of the blog
        loader = web_loader("https://iamdipanshus.in")
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        all_splits = text_splitter.split_documents(docs)

        # Index chunks
        _ = vector_store.add_documents(documents=all_splits)

        tools = [retrieve_context]
        # If desired, specify custom instructions
        prompt = (
            "You have access to a tool that retrieves context from a blog post. "
            "Use the tool to help answer user queries."
        )
        self.agent = create_agent(model, tools, system_prompt=prompt)
        
    def get_agent(self):
        return self.agent
