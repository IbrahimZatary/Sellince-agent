import json

from langchain_core.documents import Document

from .config import PRODUCTS_FILE


REQUIRED_FIELDS = {
    "product_id",
    "name",
    "description",
    "features",
    "price",
    "target_segment",
}


def load_product_documents() -> list[Document]:
    with PRODUCTS_FILE.open("r", encoding="utf-8") as file:
        products = json.load(file)

    documents: list[Document] = []

    for product in products:
        missing_fields = REQUIRED_FIELDS - product.keys()

        if missing_fields:
            product_name = product.get("name", "Unknown product")
            product_id = product.get("product_id", "Unknown ID")

            raise ValueError(
                f"Product '{product_name}' "
                f"(ID: {product_id}) is missing required fields: "
                f"{sorted(missing_fields)}"
            )

        features = product["features"]

        if not isinstance(features, list) or not features:
            raise ValueError(
                f"Product '{product['name']}' must have a non-empty features list."
            )

        page_content = (
            f"{product['name']}. "
            f"{product['description']} "
            f"Features: {', '.join(features)}. "
            f"Target segment: {product['target_segment']}."
        )

        document = Document(
            page_content=page_content,
            metadata={
                "product_id": product["product_id"],
                "name": product["name"],
                "description": product["description"],
                "features": features,
                "price": product["price"],
                "target_segment": product["target_segment"],
            },
        )

        documents.append(document)

    return documents