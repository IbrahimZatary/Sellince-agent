from functools import lru_cache

from langchain_chroma import Chroma
from langchain_core.documents import Document

from .config import CHROMA_DIR, COLLECTION_NAME
from .embeddings import get_embedding_model


@lru_cache(maxsize=1)
def get_vector_store() -> Chroma:
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embedding_model(),
        persist_directory=str(CHROMA_DIR),
    )


def store_documents(documents: list[Document]) -> list[str]:
    if not documents:
        raise ValueError("No documents were provided.")

    ids = [
        str(document.metadata["product_id"])
        for document in documents
    ]

    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate product_id values were found.")

    vector_store = get_vector_store()

    vector_store.add_documents(
        documents=documents,
        ids=ids,
    )

    return ids