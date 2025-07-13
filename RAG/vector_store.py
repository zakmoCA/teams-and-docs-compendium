import chromadb
from pathlib import Path

CHROMA_DB_PATH = Path("rag/.chroma_store").resolve()

# new .chroma_store/ if none
if CHROMA_DB_PATH.exists() and not CHROMA_DB_PATH.is_dir():
    CHROMA_DB_PATH.unlink()

# init chroma
client = chromadb.PersistentClient(path=str(CHROMA_DB_PATH))


client = chromadb.PersistentClient(path=str(CHROMA_DB_PATH))
collection = client.get_or_create_collection(name="docs")

def add_documents(docs, ids, embeddings):
    """
    Add a list of documents and their embeddings to the vector store.
    """
    collection.add(
        documents=docs,
        embeddings=embeddings,
        ids=ids
    )

def query_similar(query_embedding, top_k=5):
    """
    Query for the top_k most similar documents given a query embedding.
    """
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
