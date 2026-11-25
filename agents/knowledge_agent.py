from agents.llm import llm
from rag.retriever import get_retriever

def knowledge_agent(customer_message, chat_history=None):
    retriever = get_retriever()
    documents = retriever.invoke(customer_message)
    if not documents:
        return {
            "answer": "I could not find relevant information in our company documents.",
            "sources": []
        }
    context = "\n\n".join(document.page_content for document in documents)
    conversation = ""
    if chat_history:
        conversation = "\n".join(
            f"{message['role']}: {message['content']}"
            for message in chat_history
        )
    prompt = f"""
    You are a helpful customer support knowledge agent.

    Use the conversation history to understand follow-up questions.
    Answer using ONLY the company information provided below.
    Do not treat conversation history as company policy.

    Rules:
    1. Do not invent company policies.
    2. If the answer is not available in the context,
       clearly say that you do not have this information.
    3. Give a clear and simple answer.

    Previous Conversation:
    {conversation}

    Company Information:
    {context}

    Customer Question:
    {customer_message}
    """
    response = llm.invoke(prompt)
    sources = list(set(
        document.metadata.get("source", "Unknown")
        for document in documents
    ))
    return {
        "answer": response.content,
        "sources": sources
    }