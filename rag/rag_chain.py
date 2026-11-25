from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL
from rag.retriever import get_retriever
client = Groq(api_key=GROQ_API_KEY)

def ask_question(question):

    # Retrieve relevant documents
    retriever = get_retriever()
    documents = retriever.invoke(question)
    # Combine retrieved content
    context = "\n\n".join(
        document.page_content for document in documents
    )
    prompt = f"""
    You are a helpful customer support assistant.

    Answer the customer's question using ONLY the context below.

    If the answer is not available in the context,
    clearly say that you do not have this information.

    Do not invent company policies.

    Context:
    {context}

    Customer Question:
    {question}
    """
    # Generate response using Groq
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_completion_tokens=500
    )
    answer = response.choices[0].message.content
    return answer, documents


