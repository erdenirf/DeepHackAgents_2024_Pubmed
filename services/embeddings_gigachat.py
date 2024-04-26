from langchain_community.embeddings.gigachat import GigaChatEmbeddings
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from pathlib import Path
import dotenv
import os

try:
    dotenv.load_dotenv()
except:
    pass

GIGACHAT_API_CREDENTIALS = os.environ.get("GIGACHAT_API_CREDENTIALS")

CACHE_FOLDER = "./cache/"
Path(CACHE_FOLDER).mkdir(parents=True, exist_ok=True)
store = LocalFileStore(CACHE_FOLDER)

underlying_embeddings = GigaChatEmbeddings(
    credentials=GIGACHAT_API_CREDENTIALS, 
    verify_ssl_certs=False,
    scope='GIGACHAT_API_CORP',
    profanity_check=False
)

MyGigaChatEmbeddingsCached = CacheBackedEmbeddings.from_bytes_store(
            underlying_embeddings, store, namespace='Embeddings'
        )