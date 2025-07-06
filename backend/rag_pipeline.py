from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import os

# 1. Document Chunking with RecursiveCharacterTextSplitter
def chunk_document(text, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.create_documents([text])

# 2. Embedding generation with nomic-embed-text using Ollama

def get_nomic_ollama_embeddings():
    return OllamaEmbeddings(model="nomic-embed-text")

# 3. Vector store initialization with Chroma
def create_chroma_vectorstore(docs, embedding):
    return Chroma.from_documents(docs, embedding=embedding)

# 4. Basic cosine similarity search using Chroma
def similarity_search(vectorstore, query, k=3):
    return vectorstore.similarity_search(query, k=k)

# 5. Example: Orchestrate RAG pipeline
if __name__ == "__main__":
    # Example document
    text = """LangChain is the framework for building context-aware reasoning applications. It enables RAG, semantic search, and more."""
    docs = chunk_document(text)
    embedding = get_nomic_ollama_embeddings()
    vectorstore = create_chroma_vectorstore(docs, embedding)
    results = similarity_search(vectorstore, "What is LangChain?")
    for doc in results:
        print(doc.page_content)
