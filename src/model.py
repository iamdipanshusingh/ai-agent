import os
from langchain.chat_models import init_chat_model

chat_model = os.getenv("CHAT_MODEL")
model = init_chat_model(chat_model)
