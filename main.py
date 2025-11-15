from dotenv import load_dotenv

load_dotenv()

from src.agent import Agent

agent_instance = Agent("https://iamdipanshus.in")
agent = agent_instance.get_agent()

query = input("Bot: hey, how may I help you?\n")

for step in agent.stream(
    {"messages": [{"role": "user", "content": query}]}, stream_mode="values"
):
    step["messages"][-1].pretty_print()
