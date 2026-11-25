from langchain_community.vectorstores import FAISS
from rag.ingestion import load_documents
from rag.chunking import split_documents
from rag.embeddings import get_embedding_model
from config import VECTORSTORE_PATH

def create_vectorstore():
    documents = load_documents()
    chunks = split_documents(documents)
    embeddings = get_embedding_model()
    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )
    # Save vector database locally
    vectorstore.save_local(str(VECTORSTORE_PATH))
    return vectorstore


