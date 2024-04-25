from langchain_community.vectorstores import Qdrant
from .config_qdrant import ConfigQdrant

vectorstore_qdrant = Qdrant.construct_instance([''], 
                                            ConfigQdrant.embeddings, 
                                            url=ConfigQdrant.url,
                                            api_key=ConfigQdrant.api_key,
                                            collection_name=ConfigQdrant.collection_name,
                                            optimizers_config=ConfigQdrant.optimizers_config,
                                            quantization_config=ConfigQdrant.quantization_config,
                                            force_recreate=True)