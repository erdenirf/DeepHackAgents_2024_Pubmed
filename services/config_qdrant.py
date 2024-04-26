from dataclasses import dataclass
from .embeddings_gigachat import MyGigaChatEmbeddingsCached, underlying_embeddings
import dotenv
import os

try:
    dotenv.load_dotenv()
except:
    pass

QDRANT_URL = os.environ.get("QDRANT_URL")
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")

@dataclass
class ConfigQdrant:

    collection_name = "my_pubmed"
    
    embeddings = MyGigaChatEmbeddingsCached

    url = QDRANT_URL

    api_key = QDRANT_API_KEY
    
    optimizers_config = {
        "memmap_threshold": 20000 
    }
    
    quantization_config = {
        "scalar": {
            "type": "int8",
            "quantile": 0.99,
            "always_ram": True
        }
    }