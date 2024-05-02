from langchain_community.vectorstores import Qdrant
from .config_qdrant import ConfigQdrant

msd_empty = Qdrant.construct_instance([''], 
                                            ConfigQdrant.embeddings, 
                                            url=ConfigQdrant.url,
                                            api_key=ConfigQdrant.api_key,
                                            collection_name="my_msd",
                                            optimizers_config=ConfigQdrant.optimizers_config,
                                            quantization_config=ConfigQdrant.quantization_config,
                                            force_recreate=True)