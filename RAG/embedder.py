import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def embed_texts(texts, model="text-embedding-3-small"):
    embeddings = []
    for text in texts:
        response = openai.embeddings.create(
            model=model,
            input=text
        )
        embeddings.append(response.data[0].embedding)
    return embeddings
