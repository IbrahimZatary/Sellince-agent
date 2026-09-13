from .vector_store import get_vector_store


def search_products(
    query: str,
    product_type: str | None = None,
    eligible_product_ids: list[int] | None = None,
) -> dict:
    if not query or not query.strip():
        raise ValueError("Query must not be empty.")

    # An explicitly empty list means no products are eligible.
    if eligible_product_ids is not None and not eligible_product_ids:
        return {}

    filters = []

    if product_type is not None:
        filters.append({"type": product_type})

    if eligible_product_ids is not None:
        filters.append({
            "product_id": {"$in": eligible_product_ids}
        })

    search_options = {}

    if len(filters) == 1:
        search_options["filter"] = filters[0]
    elif len(filters) > 1:
        search_options["filter"] = {"$and": filters}

    results = get_vector_store().similarity_search(
        query=query.strip(),
        k=1,
        **search_options,
    )

    if not results:
        return {}

    metadata = results[0].metadata

    return {
        "product_id": metadata["product_id"],
        "product_name": metadata["name"],
        "type": metadata["type"],
        "speed": metadata["speed"],
        "price": metadata["price"],
        "description": metadata["description"],
        "features": metadata["features"],
        "target_segment": metadata["target_segment"],
    }