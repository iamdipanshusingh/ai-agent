from langchain.agents import create_agent
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.model import model
from src.embeddings import vector_store
from src.loaders import web_loader
from src.tools.retrieve_context import retrieve_context


class Agent:
    """Creates an agent with a prompt, to answer queries from the initial URL provided"""

    def __init__(self, url):
        # Load and chunk contents of the blog
        loader = web_loader(url)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        all_splits = text_splitter.split_documents(docs)

        # Index chunks
        _ = vector_store.add_documents(documents=all_splits)

        self.tools = [retrieve_context]
        self.agent = self.create_agent(self.tools)

    def create_agent(self, tools):
        prompt = "You have access to a tool that retrieves context the URL provided. Use the tool to help answer user queries."
        self.agent = create_agent(model, tools, system_prompt=prompt)
        return self.agent

    def get_agent(self):
        return self.agent

    def add_tools(self, tools):
        self.tools += tools
        return self.create_agent(self.tools)
