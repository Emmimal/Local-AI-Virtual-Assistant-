"""
RAG (Retrieval-Augmented Generation) Module
Allows your local AI assistant to query personal documents (PDFs, text files)
using Chroma vector database and Ollama embeddings – fully offline.
"""

import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.documents import Document

# Configuration
CHROMA_DB_PATH = "chroma_db"          # Folder where vector database is saved
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
EMBEDDING_MODEL = "llama3.2"          # Fast and good for local embeddings

# Initialize embeddings and vector store
embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
vectorstore = None

def load_or_create_vectorstore():
    """Load existing vector DB or create new one"""
    global vectorstore
    if os.path.exists(CHROMA_DB_PATH):
        print("Loading existing vector database...")
        vectorstore = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
    else:
        print("No vector database found. Create one by adding documents first.")
        vectorstore = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
    return vectorstore

def add_document(file_path: str):
    """Add a PDF or text file to the knowledge base"""
    global vectorstore
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False
    
    print(f"Processing {file_path}...")
    
    # Load document based on file type
    if file_path.lower().endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.lower().endswith((".txt", ".md")):
        loader = TextLoader(file_path)
    else:
        print("Unsupported file type. Use PDF or TXT.")
        return False
    
    documents = loader.load()
    
    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = text_splitter.split_documents(documents)
    
    print(f"Added {len(chunks)} chunks from {file_path}")
    
    # Initialize or load vectorstore
    if vectorstore is None:
        load_or_create_vectorstore()
    
    # Add to vector database
    vectorstore.add_documents(chunks)
    vectorstore.persist()
    print("Document added and database saved!")
    return True

def query_knowledge_base(question: str, k: int = 4):
    """Retrieve relevant chunks for a question"""
    global vectorstore
    if vectorstore is None:
        load_or_create_vectorstore()
    
    if vectorstore._collection.count() == 0:
        return "No documents in knowledge base yet. Add some PDFs first!"
    
    results = vectorstore.similarity_search(question, k=k)
    
    # Format context
    context = "\n\n".join([doc.page_content for doc in results])
    sources = "\n".join([doc.metadata.get('source', 'Unknown') for doc in results])
    
    return f"""Relevant information from your documents:

{context}

Sources: {sources}"""

# Example usage
if __name__ == "__main__":
    # First time: add your documents
    # add_document("my_notes.pdf")
    # add_document("project_plan.txt")
    
    # Then query
    load_or_create_vectorstore()
    while True:
        q = input("\nAsk about your documents (or 'quit'): ")
        if q.lower() in ["quit", "exit"]:
            break
        answer = query_knowledge_base(q)
        print("\n" + answer)
