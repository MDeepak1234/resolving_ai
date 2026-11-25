from langchain_community.vectorstores import FAISS
from rag.embeddings import get_embedding_model
from config import VECTORSTORE_PATH

def get_retriever():
    embeddings = get_embedding_model()
    vectorstore = FAISS.load_local(
        str(VECTORSTORE_PATH),
        embeddings,
        allow_dangerous_deserialization=True
    )
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 2}
    )
    return retriever


