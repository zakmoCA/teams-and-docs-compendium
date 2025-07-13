import sys
from pathlib import Path
import uuid

project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

from RAG.chunker import chunk_text
from RAG.embedder import embed_texts
from RAG.vector_store import add_documents

SUMMARY_PATH = Path("summarise/summaries")

all_chunks = []
all_ids = []

for summary_file in SUMMARY_PATH.glob("*.md"):
    text = summary_file.read_text()
    chunks = chunk_text(text)
    chunk_ids = [f"{summary_file.stem}_{uuid.uuid4().hex[:8]}" for _ in chunks]

    all_chunks.extend(chunks)
    all_ids.extend(chunk_ids)

# embed/index into chroma
embeddings = embed_texts(all_chunks)
add_documents(all_chunks, all_ids, embeddings)

print(f"✅ indexed {len(all_chunks)} chunks into vector store.")
