import os
import uuid
from dotenv import load_dotenv
from openai import OpenAI
from chromadb import PersistentClient

from backend.core.config import VECTOR_STORE_PATH, COLLECTION_NAME

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chroma = PersistentClient(path=str(VECTOR_STORE_PATH))
collection = chroma.get_or_create_collection(COLLECTION_NAME)

def ingest():
    for file in os.listdir("knowledge_base"):
        path = os.path.join("knowledge_base", file)

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        embedding = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        ).data[0].embedding

        collection.add(
            ids=[str(uuid.uuid4())],
            documents=[text],
            embeddings=[embedding],
            metadatas=[{"source": file}]
        )

    print("✅ Knowledge ingested and persisted")

if __name__ == "__main__":
    ingest()