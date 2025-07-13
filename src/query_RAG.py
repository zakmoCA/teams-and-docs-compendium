import sys
from pathlib import Path
from dotenv import load_dotenv
import os
from openai import OpenAI

project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))
load_dotenv()

from RAG.embedder import embed_texts
from RAG.vector_store import query_similar

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def query_rag(question: str, top_k: int = 5) -> str:
    # embed the q
    question_embedding = embed_texts([question])[0]

    # search vector store
    results = query_similar(question_embedding, top_k=top_k)
    retrieved_chunks = results['documents'][0] if results['documents'] else []

    if not retrieved_chunks:
        return "no relevant documents found."

    # build prompt w retrieved context
    context = "\n---\n".join(retrieved_chunks)
    prompt = f"""
You are a helpful assistant with access to internal project summaries. Use the context below to answer the user's question as accurately and specifically as possible.

### Context
{context}

### Question
{question}

### Answer
"""

    # Step 4: answer-gen vis gpt
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    while True:
        query = input("\nask a question (or type 'exit'): ")
        if query.strip().lower() in {"exit", "quit"}:
            break
        answer = query_rag(query)
        print(f"\n🗨️  {answer}")
