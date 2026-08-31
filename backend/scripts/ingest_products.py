from app.rag.loader import load_product_documents
from app.rag.vector_store import store_documents


def main() -> None:
    documents = load_product_documents()

    ids = store_documents(documents)

    print(
        f"Successfully stored {len(ids)} product documents in ChromaDB."
    )


if __name__ == "__main__":
    main()