from .vector_store import get_vector_store


def search_products(query: str) -> dict:
    if not query or not query.strip():
        raise ValueError("Query must not be empty.")

    vector_store = get_vector_store()

    results = vector_store.similarity_search(
        query=query.strip(),
        k=1,
    )

    if not results:
        return {}

    product = results[0]

    return {
        "product_id": product.metadata["product_id"],
        "product_name": product.metadata["name"],
        "price": product.metadata["price"],
        "description": product.metadata["description"],
        "features": product.metadata["features"],
        "target_segment": product.metadata["target_segment"],
    }