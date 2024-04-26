from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from .config_qdrant import ConfigQdrant

client = QdrantClient(
    url=ConfigQdrant.url,
    api_key=ConfigQdrant.api_key,
)

qdrant_vectorstore = Qdrant(client=client, 
                collection_name=ConfigQdrant.collection_name,
                embeddings=ConfigQdrant.embeddings)

