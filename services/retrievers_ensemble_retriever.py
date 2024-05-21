from langchain.retrievers import EnsembleRetriever
from langchain_core.retrievers import BaseRetriever
from .my_cochrane_indexing import qdrant_cochrane
from .my_msd_indexing import qdrant_msd

def get_ensemble_retriver(k1: int = 2, k2: int = 2) -> BaseRetriever:

    retriever1 = qdrant_cochrane.as_retriever(search_kwargs = { "k": k1 })

    retriever2 = qdrant_msd.as_retriever(search_kwargs = { "k": k2 })

    # initialize the ensemble retriever
    retriever = EnsembleRetriever(
        retrievers=[retriever1, retriever2], weights=[0.5, 0.5]
    )
    return retriever