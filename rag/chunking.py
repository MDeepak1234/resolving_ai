from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.ingestion import load_documents

def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    return chunks


