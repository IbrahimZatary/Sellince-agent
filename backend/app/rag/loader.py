import json

from langchain_core.documents import Document

from .config import PRODUCTS_FILE


REQUIRED_FIELDS = {
    "product_id",
    "name",
    "description",
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
                f"Product '{product_name}' (ID: {product_id}) "
                f"is missing required fields: {sorted(missing_fields)}"
            )

        page_content = (
            f"{product['name']}. "
            f"{product['description']} "
            f"Target segment: {product['target_segment']}."
        )

        document = Document(
            page_content=page_content,
            metadata={
                "product_id": product["product_id"],
                "name": product["name"],
                "price": product["price"],
                "description": product["description"],
                "target_segment": product["target_segment"],
            },
        )

        documents.append(document)

    return documents