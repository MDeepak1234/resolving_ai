from pathlib import Path
from langchain_community.document_loaders import TextLoader
from config import DATA_PATH

def load_documents():
    documents = []
    # Find all text files inside data folder
    for file_path in DATA_PATH.glob("*.txt"):
        loader = TextLoader(
            str(file_path),
            encoding="utf-8"
        )
        loaded_docs = loader.load()
        documents.extend(loaded_docs)
    return documents



