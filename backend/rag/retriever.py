import os
from dotenv import load_dotenv
from openai import OpenAI
from chromadb import PersistentClient

from backend.core.config import VECTOR_STORE_PATH, COLLECTION_NAME

# Load env
load_dotenv()

# OpenAI client (same as ingestion)
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Persistent Chroma client
chroma_client = PersistentClient(path=str(VECTOR_STORE_PATH))
collection = chroma_client.get_collection(COLLECTION_NAME)


def retrieve(query: str, top_k: int = 3):
    """
    Retrieve top-k relevant knowledge chunks for a user query.
    Uses the SAME embedding model as ingestion.
    """

    # 🔑 Generate query embedding using OpenAI
    query_embedding = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    ).data[0].embedding

    # 🔍 Query Chroma using embedding (NOT query_texts)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results.get("documents", [[]])[0]
    return documents