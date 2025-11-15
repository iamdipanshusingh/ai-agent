from langchain.agents.middleware import dynamic_prompt, ModelRequest

from ..embeddings import vector_store


@dynamic_prompt
def retrieve_context_from_docs(request: ModelRequest) -> str:
    """Inject context into state messages."""
    last_query = request.state["messages"][-1].text
    retrieved_docs = vector_store.similarity_search(last_query)

    docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)

    system_message = (
        "You are an AI assistant that must answer ONLY using the provided context."
        "Rules:"
        "1. If the answer is not 100% supported by the context, say:"
        "I don't have enough information in the provided context."
        "2. Do NOT use external knowledge."
        "3. Do NOT make assumptions."
        "4. Do NOT hallucinate."
        "5. Stick strictly to what is present in the context."
        "Context:"
        f"{docs_content}"
    )

    return system_message
