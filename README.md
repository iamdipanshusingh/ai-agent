# 🤖 AI Agent

A powerful, context-aware AI agent built with LangChain and LangGraph that can answer questions based on content from any website. The agent uses RAG (Retrieval-Augmented Generation) to provide accurate, contextually relevant responses by indexing web content and retrieving relevant information on demand.

## ✨ Features

- 🌐 **Web Content Loading**: Automatically loads and processes content from any URL
- 📚 **Intelligent Chunking**: Splits documents into optimized chunks for better retrieval
- 🔍 **Semantic Search**: Uses OpenAI embeddings for accurate context retrieval
- 🧠 **Context-Aware Responses**: Retrieves relevant context before answering queries
- 💬 **Interactive CLI**: Simple command-line interface for chatting with the agent
- 🔧 **Extensible**: Easy to add custom tools and middleware
- ⚡ **Streaming Responses**: Real-time streaming of agent responses

## 🏗️ Architecture

```
┌─────────────┐
│   User      │
│   Query     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│      LangGraph Agent                │
│  ┌───────────────────────────────┐  │
│  │  Middleware:                  │  │
│  │  retrieve_context_from_docs   │  │
│  └───────────────┬───────────────┘  │
│                  │                  │
│                  ▼                  │
│  ┌───────────────────────────────┐  │
│  │  Vector Store                 │  │
│  │  (Similarity Search)          │  │
│  └───────────────┬───────────────┘  │
│                  │                  │
│                  ▼                  │
│  ┌───────────────────────────────┐  │
│  │  LLM (GPT-5-nano)             │  │
│  │  + Context Injection          │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
       │
       ▼
┌─────────────┐
│   Response  │
└─────────────┘
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-agent
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Copy `.env.example` to `.env` and fill in all the required credentials:
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` and fill in all the required credentials:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   CHAT_MODEL=gpt-4o-mini
   ```
   
   > **Note**: 
   > - Only OpenAI models are supported for `CHAT_MODEL` (e.g., `gpt-4o`, `gpt-4o-mini`, `gpt-3.5-turbo`). See [OpenAI Chat Models](https://platform.openai.com/docs/models) for available options.
   > - `LANGSMITH_API_KEY` is optional but recommended for debugging and monitoring. Set `LANGSMITH_TRACING=false` to disable tracing.

## 📖 Usage

### Basic Usage

Run the agent with a URL:

```python
from dotenv import load_dotenv
from src.agent import Agent

load_dotenv()

# Initialize agent with a URL
agent_instance = Agent("https://example.com")
agent = agent_instance.get_agent()

# Stream responses
for step in agent.stream(
    {"messages": [{"role": "user", "content": "What is this website about?"}]}, 
    stream_mode="values"
):
    step["messages"][-1].pretty_print()
```

### Interactive CLI

Run the main script for an interactive chat session:

```bash
python main.py
```

The agent will:
1. Load and index content from the configured URL
2. Start an interactive chat session
3. Answer questions based on the indexed content
4. Type `stop`, `exit`, or `quit` to end the session

**Example Session:**
```
Bot: hey, how may I help you?

You: What is the main topic of this website?
Bot: [Streaming response based on indexed content]

You: Can you summarize the key points?
Bot: [Context-aware summary]

You: exit
Adios...
```

### Adding Custom Tools

Extend the agent with custom tools:

```python
from langchain.tools import Tool

# Define your custom tool
custom_tool = Tool(
    name="custom_tool",
    description="Description of what the tool does",
    func=your_function
)

# Add tools to the agent
agent_instance.add_tools([custom_tool])
```

## 📁 Project Structure

```
ai-agent/
├── main.py                 # Entry point with interactive CLI
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (copy from .env.example)
├── .env.example            # Example environment variables template
├── .venv/                  # Virtual environment (gitignored)
├── README.md              # This file
└── src/
    ├── __init__.py
    ├── agent.py           # Main Agent class
    ├── model.py           # LLM model configuration
    ├── embeddings.py      # Embeddings and vector store setup
    ├── loaders.py         # Document loaders (web, CSV, etc.)
    └── middleware/
        ├── __init__.py
        └── retrieve_context.py  # Context retrieval middleware
```

## 🔧 Configuration

### Model Configuration

The chat model is configured via the `CHAT_MODEL` environment variable in your `.env` file:

```env
CHAT_MODEL=gpt-4o-mini
```

> **Note**: Only OpenAI models are supported. For a list of available models, see [LangChain Chat Models Documentation](https://python.langchain.com/docs/integrations/chat/).

### Embedding Configuration

**Embedding Configuration** (`src/embeddings.py`):
- Currently uses `text-embedding-3-large` embedding model
- Will be configurable via environment variables in future updates

### Loader Configuration

**Loader Configuration** (`src/loaders.py`):
- Currently supports web content loading via `WebBaseLoader`
- Additional loaders (CSV, PDF, etc.) will be added in future updates

### Chunking Configuration

**Chunking Configuration** (`src/agent.py`):
- Chunk size: 1000 characters
- Chunk overlap: 200 characters
- These can be adjusted directly in the code if needed

## 📦 Key Dependencies

- **LangChain**: Framework for building LLM applications
- **LangGraph**: For creating stateful, multi-actor applications
- **OpenAI**: For embeddings and chat models
- **BeautifulSoup4**: For web content parsing
- **python-dotenv**: For environment variable management

See `requirements.txt` for the complete list of dependencies.

## 🧩 How It Works

1. **Content Loading**: The agent loads content from the provided URL using `WebBaseLoader` (additional loaders will be added in future updates)
2. **Text Splitting**: Content is split into chunks of 1000 characters with 200 character overlap
3. **Embedding**: Chunks are converted to embeddings using OpenAI's `text-embedding-3-large` model (configurable via environment variables)
4. **Indexing**: Embeddings are stored in an in-memory vector store
5. **Query Processing**: When a user asks a question:
   - The query is converted to an embedding
   - Similar chunks are retrieved from the vector store
   - Relevant context is injected into the system prompt
   - The LLM (configured via `CHAT_MODEL` environment variable) generates a response based only on the provided context
6. **Response Generation**: The agent streams responses in real-time

## 🎯 Use Cases

- 📄 **Document Q&A**: Ask questions about website content
- 🔍 **Content Analysis**: Analyze and summarize web pages
- 📚 **Knowledge Base**: Create a Q&A system from any website
- 🤖 **Custom Chatbots**: Build domain-specific chatbots
- 📊 **Research Assistant**: Extract and answer questions from research papers

## 🛠️ Development

### Running Tests

```bash
# Add your test commands here
python -m pytest
```

### Code Style

This project follows PEP 8 style guidelines. Consider using:
- `black` for code formatting
- `flake8` for linting
- `mypy` for type checking

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Built with [LangChain](https://www.langchain.com/) and [LangGraph](https://langchain-ai.github.io/langgraph/)
- Powered by [OpenAI](https://openai.com/) embeddings and models

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ using LangChain and LangGraph**

