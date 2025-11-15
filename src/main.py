from agent import Agent

agent_instance = Agent("https://iamdipanshus.in")
agent = agent_instance.agent

query = input("Bot: hey, how may I help you?")

for step in agent.stream(
    {"messages": [{"role": "user", "content": query}]}, stream_mode="values"
):
    step["messages"][-1].pretty_print()
